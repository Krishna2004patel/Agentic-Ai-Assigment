
from dataclasses import dataclass


@dataclass
class MemoryRecord:
    topic: str
    fact: str
    date: str


class ProjectMemory:
    def __init__(self):
        self.records = []

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
            return f"No stored information about {topic}"

        latest = records[-1]

        return f"[memory] {latest.fact}"


memory = ProjectMemory()

memory.write(
    MemoryRecord(
        "database",
        "We chose PostgreSQL",
        "2026-07-03"
    )
)

memory.write(
    MemoryRecord(
        "hosting",
        "We chose AWS hosting",
        "2026-07-05"
    )
)

assistant = ProjectAssistant(memory)

print("--- Database retrieval ---")
print(assistant.answer("database"))

print("\n--- Hosting retrieval ---")
print(assistant.answer("hosting"))
