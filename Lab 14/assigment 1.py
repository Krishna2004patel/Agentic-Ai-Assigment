
"""
Lab 14 Assignment 1
Add a Second Reusable Skill

Skills:
1. triage_skill
2. password_reset_skill
"""

from datetime import datetime

FAQ_DB = {
    "wifi": "Connect to Campus-Secure using your student ID."
}

TICKET_DB = []


# --------------------------------------------------
# Tool 1: Search FAQ
# --------------------------------------------------

def tool_search_faq(query):

    for key, value in FAQ_DB.items():

        if key in query.lower():
            return {
                "found": True,
                "answer": value
            }

    return {"found": False}


# --------------------------------------------------
# Tool 2: Create Ticket
# --------------------------------------------------

def tool_create_ticket(issue):

    ticket_id = f"T-{len(TICKET_DB) + 1:03d}"

    TICKET_DB.append({
        "id": ticket_id,
        "issue": issue,
        "status": "open"
    })

    return {"ticket_id": ticket_id}


# --------------------------------------------------
# Tool 3: Check Ticket Status
# --------------------------------------------------

def tool_check_ticket_status(ticket_id):

    for ticket in TICKET_DB:

        if ticket["id"] == ticket_id:
            return ticket

    return {"error": "not found"}


# --------------------------------------------------
# Skill 1: General Triage Skill
# --------------------------------------------------

def triage_skill(issue_text):
    """
    Instructions:
    Search the FAQ first.
    If no answer is found, create a ticket.

    Constraint:
    Never invent FAQ answers.
    """

    faq_result = tool_search_faq(issue_text)

    if faq_result["found"]:

        return {
            "skill": "triage_skill",
            "resolution": "faq",
            "answer": faq_result["answer"]
        }

    ticket = tool_create_ticket(issue_text)

    return {
        "skill": "triage_skill",
        "resolution": "escalated",
        "ticket_id": ticket["ticket_id"]
    }


# --------------------------------------------------
# Skill 2: Password Reset Guidance
# --------------------------------------------------

def password_reset_skill(issue_text):
    """
    Instructions:
    Identify password-reset requests and provide
    safe password-reset guidance.

    Constraint:
    Never ask users to share their password.
    Never claim to reset a password directly.
    """

    return {
        "skill": "password_reset_skill",
        "resolution": "guidance",
        "answer": (
            "To reset your campus password, open the "
            "official campus login page and select "
            "'Forgot Password'. Follow the verification "
            "steps. Never share your password with anyone."
        )
    }


# --------------------------------------------------
# Memory
# --------------------------------------------------

class CapstoneMemory:

    def __init__(self):
        self.session = {}
        self.history = []

    def record(self, user, issue, outcome):

        entry = {
            "user": user,
            "issue": issue,
            "outcome": outcome,
            "date": datetime.now().isoformat(
                timespec="seconds"
            )
        }

        self.history.append(entry)
        self.session["last_issue"] = issue


# --------------------------------------------------
# Node Graph
# Intake -> Skill Routing -> Response -> Log
# --------------------------------------------------

def node_graph_run(user, issue, memory, audit_log, prompt_log):

    prompt_log.append({
        "stage": "intake",
        "input": issue
    })

    if not issue.strip():

        audit_log.append({
            "stage": "intake",
            "result": "rejected: empty issue"
        })

        return {
            "rejected": True,
            "reason": "empty issue text"
        }

    # Route to the correct reusable skill
    issue_lower = issue.lower()

    if "password" in issue_lower or "reset" in issue_lower:

        outcome = password_reset_skill(issue)

    else:

        outcome = triage_skill(issue)

    prompt_log.append({
        "stage": "skill",
        "selected_skill": outcome["skill"],
        "output": outcome
    })

    # Generate response
    if outcome["resolution"] in ["faq", "guidance"]:

        response = outcome["answer"]

    else:

        response = (
            f"Ticket {outcome['ticket_id']} created. "
            "Support will follow up."
        )

    memory.record(user, issue, outcome)

    audit_log.append({
        "stage": "complete",
        "user": user,
        "issue": issue,
        "outcome": outcome
    })

    return {
        "rejected": False,
        "response": response,
        "outcome": outcome
    }


# --------------------------------------------------
# Main Program: Demonstrate Both Skills
# --------------------------------------------------

if __name__ == "__main__":

    memory = CapstoneMemory()
    audit_log = []
    prompt_log = []

    print("=== Example 1: General FAQ Skill ===")

    result1 = node_graph_run(
        "alice",
        "How do I connect to wifi?",
        memory,
        audit_log,
        prompt_log
    )

    print(result1)

    print("\n=== Example 2: Password Reset Skill ===")

    result2 = node_graph_run(
        "bob",
        "I forgot my password. How can I reset it?",
        memory,
        audit_log,
        prompt_log
    )

    print(result2)

    print("\n=== Example 3: Ticket Escalation ===")

    result3 = node_graph_run(
        "carol",
        "My laptop charger is broken",
        memory,
        audit_log,
        prompt_log
    )

    print(result3)

    print("\n=== Prompt Log ===")

    for item in prompt_log:
        print(item)

    print("\n=== Audit Log ===")

    for item in audit_log:
        print(item)

    print("\n=== Memory History ===")

    for item in memory.history:
        print(item)
