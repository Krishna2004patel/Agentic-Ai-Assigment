
from datetime import datetime


class Memory:

    def __init__(self):
        self.store = {}

    def scope(self, user):
        return self.store.setdefault(user, {})


class Audit:

    def __init__(self):
        self.entries = []

    def log(self, task, user, skill, tool_calls,
            result=None, error=None):

        self.entries.append({
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "task": task,
            "user": user,
            "skill": skill,
            "tool_calls": tool_calls,
            "result": result,
            "error": error
        })


class DraftEmailSkill:

    CONTACTS = {
        "Dr. Meena": {
            "email": "meena@example.edu"
        }
    }

    def __init__(self, memory_scope):
        self.memory_scope = memory_scope
        self.tool_calls = []

    def execute(self, task):

        contact = self.CONTACTS.get(
            task["to"],
            {"error": f"no contact found for {task['to']}"}
        )

        self.tool_calls.append({
            "tool": "lookup_contact",
            "output": contact
        })

        if "error" in contact:
            raise RuntimeError(contact["error"])

        return f"Draft email to {contact['email']}"


SKILL_REGISTRY = {
    "draft_email": DraftEmailSkill
}


def select_skill(task):
    return task["skill"]


def run_task(task, user, memory, audit):

    skill_name = select_skill(task)

    skill_cls = SKILL_REGISTRY[skill_name]

    skill = skill_cls(memory.scope(user))

    try:

        result = skill.execute(task)

        audit.log(
            task,
            user,
            skill_name,
            skill.tool_calls,
            result=result
        )

        return result

    except Exception as e:

        audit.log(
            task,
            user,
            skill_name,
            skill.tool_calls,
            error=str(e)
        )

        raise


def receive_task(task, user, memory, audit):

    skill_name = task["skill"]

    # Count previous failures from the audit log
    failures = 0

    for entry in audit.entries:

        if (
            entry["user"] == user
            and entry["skill"] == skill_name
            and entry["error"] is not None
        ):
            failures += 1

    # Escalate after two failures
    if failures >= 2:

        message = (
            f"Escalated to human: skill '{skill_name}' "
            f"failed twice for user '{user}'."
        )

        audit.log(
            task,
            user,
            skill_name,
            [],
            error=message
        )

        return message

    return run_task(task, user, memory, audit)


if __name__ == "__main__":

    memory = Memory()
    audit = Audit()

    task = {
        "skill": "draft_email",
        "to": "Unknown Person"
    }

    print("=== First attempt ===")

    try:
        print(
            receive_task(task, "uday", memory, audit)
        )
    except RuntimeError as e:
        print("Failed:", e)

    print("\n=== Second attempt ===")

    try:
        print(
            receive_task(task, "uday", memory, audit)
        )
    except RuntimeError as e:
        print("Failed:", e)

    print("\n=== Third attempt ===")

    result = receive_task(
        task,
        "uday",
        memory,
        audit
    )

    print(result)
