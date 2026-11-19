
from datetime import datetime


class Memory:

    def __init__(self):
        self.store = {}

    def scope(self, user):
        return self.store.setdefault(user, {})


class Audit:

    def __init__(self):
        self.entries = []

    def log(self, task, skill, result=None, error=None):
        self.entries.append({
            "task": task,
            "skill": skill,
            "result": result,
            "error": error,
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            )
        })


class SummarizeNotesSkill:

    def __init__(self, memory_scope):
        self.memory_scope = memory_scope
        self.tool_calls = []

    def execute(self, task):
        text = task.get("text", "")
        count = len(text.split())

        self.memory_scope["last_note_length"] = count

        return f"Summary stub: note has {count} words."


SKILL_REGISTRY = {
    "summarize_notes": SummarizeNotesSkill
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
            skill_name,
            result=result
        )

        return result

    except Exception as e:
        audit.log(
            task,
            skill_name,
            error=str(e)
        )

        raise


# Rate limiter
class RateLimiter:

    def __init__(self, max_tasks):
        self.max_tasks = max_tasks
        self.task_count = {}

    def allowed(self, user):

        count = self.task_count.get(user, 0)

        if count >= self.max_tasks:
            return False

        self.task_count[user] = count + 1

        return True


# Interface with rate limiting
def receive_task(task, user, memory, audit, limiter):

    if not limiter.allowed(user):
        return "Task rejected: maximum 3 tasks per session reached."

    return run_task(task, user, memory, audit)


if __name__ == "__main__":

    memory = Memory()
    audit = Audit()
    limiter = RateLimiter(max_tasks=3)

    for i in range(1, 5):

        print(f"\n--- Task {i} ---")

        task = {
            "skill": "summarize_notes",
            "text": "Agentic AI uses tools and memory"
        }

        result = receive_task(
            task,
            user="uday",
            memory=memory,
            audit=audit,
            limiter=limiter
        )

        print(result)
