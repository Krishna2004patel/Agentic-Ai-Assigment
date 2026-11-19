
"""
Lab 14: Capstone Project Studio
Campus Help-Desk Agent

Includes:
- Three tools
- One reusable triage skill
- Short-term and long-term memory
- Simplified node graph
- Prompt log and audit log
- Evaluation suite
- Safety check for empty input
"""

from datetime import datetime

# --------------------------------------------------
# Tools (3)
# --------------------------------------------------

FAQ_DB = {
    "wifi": "Connect to 'Campus-Secure' and log in with your student ID."
}

TICKET_DB = []


def tool_search_faq(query):
    for key, value in FAQ_DB.items():
        if key in query.lower():
            return {
                "found": True,
                "answer": value
            }

    return {"found": False}


def tool_create_ticket(issue):
    ticket_id = f"T-{len(TICKET_DB) + 1:03d}"

    TICKET_DB.append({
        "id": ticket_id,
        "issue": issue,
        "status": "open"
    })

    return {"ticket_id": ticket_id}


def tool_check_ticket_status(ticket_id):
    for ticket in TICKET_DB:
        if ticket["id"] == ticket_id:
            return ticket

    return {"error": "not found"}


# --------------------------------------------------
# Reusable Skill: Triage and Respond
# --------------------------------------------------

def triage_skill(issue_text):
    """
    Instructions:
    Search the FAQ first.
    Create a support ticket only if no FAQ match exists.

    Constraint:
    Never fabricate an FAQ answer.
    """

    faq_result = tool_search_faq(issue_text)

    if faq_result["found"]:
        return {
            "resolution": "faq",
            "answer": faq_result["answer"]
        }

    ticket = tool_create_ticket(issue_text)

    return {
        "resolution": "escalated",
        "ticket_id": ticket["ticket_id"]
    }


# --------------------------------------------------
# Memory: Session and Long-term History
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
# Intake -> Triage -> Respond -> Log
# --------------------------------------------------

def node_graph_run(user, issue, memory, audit_log, prompt_log):

    prompt_log.append({
        "stage": "intake",
        "input": issue
    })

    # Safety control: reject empty input
    if not issue.strip():
        audit_log.append({
            "stage": "intake",
            "result": "rejected: empty issue"
        })

        return {
            "rejected": True,
            "reason": "empty issue text"
        }

    # Triage node
    outcome = triage_skill(issue)

    prompt_log.append({
        "stage": "triage",
        "output": outcome
    })

    # Response node
    if outcome["resolution"] == "faq":
        response = outcome["answer"]

    else:
        response = (
            f"Ticket {outcome['ticket_id']} created; "
            "support will follow up."
        )

    # Memory and audit logging
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
# Evaluation Suite
# --------------------------------------------------

def run_evaluation():

    cases = [
        ("How do I connect to wifi?", "faq"),
        ("My laptop charger is broken", "escalated")
    ]

    memory = CapstoneMemory()
    audit_log = []
    prompt_log = []

    results = []

    for issue, expected in cases:

        result = node_graph_run(
            "eval_user",
            issue,
            memory,
            audit_log,
            prompt_log
        )

        actual = result["outcome"]["resolution"]

        results.append({
            "issue": issue,
            "expected": expected,
            "actual": actual,
            "passed": actual == expected
        })

    return results


# --------------------------------------------------
# Main Program
# --------------------------------------------------

if __name__ == "__main__":

    memory = CapstoneMemory()
    audit_log = []
    prompt_log = []

    print("=== Run 1: FAQ Match ===")

    r1 = node_graph_run(
        "alice",
        "How do I connect to wifi on campus?",
        memory,
        audit_log,
        prompt_log
    )

    print(r1)

    print("\n=== Run 2: Ticket Creation ===")

    r2 = node_graph_run(
        "bob",
        "My laptop charger is broken",
        memory,
        audit_log,
        prompt_log
    )

    print(r2)

    print("\n=== Run 3: Empty Input Safety Check ===")

    r3 = node_graph_run(
        "carol",
        " ",
        memory,
        audit_log,
        prompt_log
    )

    print(r3)

    print("\n=== Evaluation Results ===")

    eval_results = run_evaluation()

    for result in eval_results:
        status = "PASS" if result["passed"] else "FAIL"

        print(
            f"[{status}] {result['issue']} -> "
            f"{result['actual']} "
            f"(expected {result['expected']})"
        )

    print("\n=== Prompt Log ===")

    for item in prompt_log:
        print(item)

    print("\n=== Audit Log ===")

    for item in audit_log:
        print(item)

    print("\n=== Long-term Memory / History ===")

    for item in memory.history:
        print(item)

    print("\n=== Limitations and Next-step Roadmap ===")

    print("- FAQ matching is keyword-based, not semantic.")
    print("- No human approval gate for high-priority tickets.")
    print("- Next step: add retrieval-based FAQ matching.")
    print("- Next step: add a priority-classification skill.")
