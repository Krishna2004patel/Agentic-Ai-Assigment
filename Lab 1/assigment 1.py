
import json

SIMULATED_ANSWERS = {
    "subjects": ["Data Structures", "Operating Systems", "AI Agents"],
    "hours_per_day": 2,
    "unavailable_days": ["Sunday"]
}


class StudyPlannerAgent:

    def __init__(self):

        self.goal = {
            "subjects": None,
            "hours_per_day": None,
            "unavailable_days": None,
            "schedule_generated": False
        }

        self.plan = None
        self.log = []

    def satisfied(self):
        return self.goal["schedule_generated"]

    def next_step(self):

        for field in ("subjects", "hours_per_day", "unavailable_days"):
            if self.goal[field] is None:
                return "ask", field

        return "generate_plan", None

    def run(self):

        while not self.satisfied():

            step, arg = self.next_step()

            if step == "ask":

                answer = SIMULATED_ANSWERS[arg]
                self.goal[arg] = answer

                self.log.append({
                    "iteration": len(self.log) + 1,
                    "planned": f"ask for {arg}",
                    "action": f"asked user for {arg}",
                    "observed": answer,
                    "stopped": False
                })

            elif step == "generate_plan":

                self.plan = self._build_plan()

                self.goal["schedule_generated"] = True

                self.log.append({
                    "iteration": len(self.log) + 1,
                    "planned": "generate study plan",
                    "action": "created weekly plan",
                    "observed": self.plan,
                    "stopped": True
                })

        return self.plan

    def _build_plan(self):

        days = [
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"
        ]

        available_days = []

        for day in days:
            if day not in self.goal["unavailable_days"]:
                available_days.append(day)

        subjects = self.goal["subjects"]

        plan = {}

        for i, day in enumerate(available_days):

            plan[day] = {
                "subject": subjects[i % len(subjects)],
                "time": "17:00-19:00"
            }

        return plan

    # Apply feedback to the existing plan
    def revise(self, feedback):

        self.log.append({
            "iteration": len(self.log) + 1,
            "planned": "apply user feedback",
            "action": f"received feedback: {feedback}",
            "observed": None,
            "stopped": False
        })

        if "tuesday" in feedback.lower() and "evening" in feedback.lower():

            if "Tuesday" in self.plan:
                self.plan["Tuesday"]["time"] = "20:00-22:00"

        if "friday" in feedback.lower() and "one hour" in feedback.lower():

            if "Friday" in self.plan:
                self.plan["Friday"]["time"] = "17:00-18:00"

        self.log.append({
            "iteration": len(self.log) + 1,
            "planned": "confirm revised plan",
            "action": "modified existing plan without regenerating",
            "observed": self.plan,
            "stopped": True
        })

        return self.plan


if __name__ == "__main__":

    agent = StudyPlannerAgent()

    plan = agent.run()

    print("=== INITIAL STUDY PLAN ===")
    print(json.dumps(plan, indent=2))

    # First feedback
    feedback1 = "Move Tuesday's session to the evening."

    print("\n=== FIRST FEEDBACK ===")
    print(feedback1)

    agent.revise(feedback1)

    # Second feedback
    feedback2 = "Also make Friday's session shorter, only one hour."

    print("\n=== SECOND FEEDBACK ===")
    print(feedback2)

    agent.revise(feedback2)

    print("\n=== FINAL STUDY PLAN ===")
    print(json.dumps(agent.plan, indent=2))

    print("\n=== FULL ITERATION LOG ===")

    for entry in agent.log:
        print(json.dumps(entry, indent=2))
