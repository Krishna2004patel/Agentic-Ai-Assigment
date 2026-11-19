
import csv
import io

# CSV data with category
SIGNUPS_CSV = """event,signups,category
AI Club Talk,12,technical
Hackathon Kickoff,9,technical
Robotics Demo,15,technical
GenAI Workshop,7,technical
Capstone Expo,20,social
Career Panel,11,social
"""


# Tool 1: Read CSV
def read_csv():

    reader = csv.DictReader(io.StringIO(SIGNUPS_CSV))
    rows = list(reader)

    if not rows:
        return {"error": "CSV is empty", "rows": []}

    return {"rows": rows}


# Tool 2: Filter by category
def filter_category(rows, category):

    filtered_rows = []

    for row in rows:

        if row["category"].lower() == category.lower():
            filtered_rows.append(row)

    return {"filtered_rows": filtered_rows}


# Tool 3: Calculator
def calculator(operation, values):

    if operation == "average":

        if not values:
            return {"error": "No values supplied"}

        return {"result": sum(values) / len(values)}

    return {"error": "Unsupported operation"}


TOOLS = {
    "read_csv": read_csv,
    "filter_category": filter_category,
    "calculator": calculator
}


class CampusDataAssistant:

    def __init__(self):
        self.trace = []

    def _call(self, tool_name, reason, **kwargs):

        result = TOOLS[tool_name](**kwargs)

        self.trace.append({
            "tool": tool_name,
            "reason": reason,
            "input": kwargs,
            "output": result
        })

        if "error" in result:
            raise RuntimeError(result["error"])

        return result

    def answer(self, question):

        q = question.lower()

        if "technical" in q and "average" in q:

            # Step 1: Read CSV
            data = self._call(
                "read_csv",
                "Event sign-up data and categories are stored in the CSV"
            )

            # Step 2: Filter technical events
            filtered = self._call(
                "filter_category",
                "Only technical events are required for this question",
                rows=data["rows"],
                category="technical"
            )

            filtered_rows = filtered["filtered_rows"]

            # Validate filter result
            if not filtered_rows:
                return "No technical events found. Average cannot be calculated."

            # Extract sign-up values
            values = [
                int(row["signups"])
                for row in filtered_rows
            ]

            # Step 3: Calculate average
            result = self._call(
                "calculator",
                "Calculate average using only filtered technical events",
                operation="average",
                values=values
            )

            return (
                f"Average sign-ups for technical events: "
                f"{result['result']:.2f}"
            )

        return "Question not supported"


if __name__ == "__main__":

    assistant = CampusDataAssistant()

    question = "What's the average sign-up for technical events only?"

    print("Q:", question)
    print("A:", assistant.answer(question))

    print("\n=== TOOL EXECUTION TRACE ===")

    for i, entry in enumerate(assistant.trace, 1):

        print(f"\n{i}. Tool: {entry['tool']}")
        print("Reason:", entry["reason"])
        print("Input:", entry["input"])
        print("Output:", entry["output"])
