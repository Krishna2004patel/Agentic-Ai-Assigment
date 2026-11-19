
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class MemoryRecord:
    topic: str
    fact: str
    date: str


class ProjectMemory:
    def __init__(self, retention_days):
        self.records = []
        self.retention_days = retention_days

    def write(self, record):
        self.records.append(record)

    def retrieve(self, topic):
        return [r for r in self.records if r.topic == topic]


class ProjectAssistant:
    def __init__(self, memory):
        self.memory = memory

    def answer(self, topic):
        records = self.memory.retrieve(topic)

        if not records:
            return f"No stored decision about {topic}"

        latest = records[-1]

        stored_date = date.fromisoformat(latest.date)
        today = date.today()

        age = (today - stored_date).days

        if age > self.memory.retention_days:
            return (
                f"Warning: This decision is from {age} days ago "
                f"and may be out of date.\n"
                f"Stored decision: {latest.fact}"
            )

        return (
            f"Fresh memory ({age} days old): {latest.fact}"
        )


memory = ProjectMemory(retention_days=30)

today = date.today()

fresh_date = today.isoformat()

old_date = (today - timedelta(days=60)).isoformat()

memory.write(
    MemoryRecord(
        "database",
        "We chose PostgreSQL",
        fresh_date
    )
)

memory.write(
    MemoryRecord(
        "hosting",
        "We chose AWS hosting",
        old_date
    )
)

assistant = ProjectAssistant(memory)

print("--- Fresh record ---")
print(assistant.answer("database"))

print("\n--- Old record ---")
print(assistant.answer("hosting"))
