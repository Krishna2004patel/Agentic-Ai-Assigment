
import csv
import io

SIGNUPS_CSV = """event,signups
AI Club Talk,12
Hackathon Kickoff,9
Robotics Demo,15
GenAI Workshop,7
Capstone Expo,20
Career Panel,11
"""

THRESHOLD = 13


def calculator(operation, values):

    if operation == "sum":
        return {"result": sum(values)}

    if operation == "average":

        if not values:
            return {"error": "no values supplied"}

        return {"result": sum(values) / len(values)}

    return {"error": "unsupported operation"}


def read_csv():

    reader = csv.DictReader(io.StringIO(SIGNUPS_CSV))
    rows = list(reader)

    if not rows:
        return {"error": "empty file", "rows": []}

    return {"rows": rows, "row_count": len(rows)}


# Fourth tool: Draft notification only
def send_notification(message):

    return {
        "status": "Draft created",
        "message": message
    }


TOOLS = {
    "calculator": calculator,
    "read_csv": read_csv,
    "send_notification": send_notification
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

        if "average" in question.lower():

            data = self._call(
                "read_csv",
                "Sign-up information is stored in the CSV file"
            )

            values = [
                int(row["signups"])
                for row in data["rows"]
            ]

            avg = self._call(
                "calculator",
                "Calculate the average sign-ups",
                operation="average",
                values=values
            )

            average = avg["result"]

            print(f"Average sign-ups: {average:.2f}")

            if average < THRESHOLD:

                message = (
                    f"Low turnout alert: The average sign-ups "
                    f"are {average:.2f}, below the threshold "
                    f"of {THRESHOLD}. Please promote upcoming events."
                )

                notification = self._call(
                    "send_notification",
                    "Average sign-ups are below the defined threshold",
                    message=message
                )

                print("\nNotification:")
                print(notification["message"])
                print("Status:", notification["status"])

            else:
                print("Sign-ups are satisfactory. No notification needed.")

            return

        return "Question not supported"


if __name__ == "__main__":

    assistant = CampusDataAssistant()

    question = "What is the average sign-up for events?"

    print("Q:", question)
    assistant.answer(question)

    print("\n=== TOOL EXECUTION TRACE ===")

    for i, entry in enumerate(assistant.trace, 1):

        print(f"\n{i}. Tool: {entry['tool']}")
        print("Reason:", entry["reason"])
        print("Input:", entry["input"])
        print("Output:", entry["output"])
