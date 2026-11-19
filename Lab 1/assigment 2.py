
import json

SIMULATED_ANSWERS = {
    "subjects": ["Data Structures", "Operating Systems", "AI Agents"],
    "hours_per_day": 2,
    "unavailable_days": ["Sunday"]
}


class StudyPlannerAgent:

    def __init__(self, existing_schedule):

        self.goal = {
            "subjects": None,
            "hours_per_day": None,
            "unavailable_days": None,
            "schedule_generated": False
        }

        self.existing_schedule = existing_schedule
        self.plan = None
        self.log = []

    def satisfied(self):
        return self.goal["schedule_generated"]

    def next_step(self):

        for field in ("subjects", "hours_per_day", "unavailable_days"):
            if self.goal[field] is None:
                return "ask", field

        return "generate_plan", None

    def read_existing_schedule(self):

        return self.existing_schedule

    # Detect scheduling conflicts
    def check_conflicts(self, busy_days):

        unavailable = self.goal["unavailable_days"]

        conflicts = []

        for day in busy_days:
            if day not in unavailable:
                conflicts.append(day)

        if conflicts:

            print("\nSCHEDULING CONFLICT DETECTED!")
            print("The following days are already busy:", conflicts)

            print("Updating unavailable days to avoid double-booking.")

            for day in conflicts:
                unavailable.append(day)

            print("Updated unavailable days:", unavailable)

            self.log.append({
                "iteration": len(self.log) + 1,
                "planned": "check scheduling conflicts",
                "action": "reported conflicts and updated unavailable days",
                "observed": conflicts,
                "stopped": False
            })

        else:

            print("\nNo scheduling conflicts detected.")

    # Main agent loop
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

                busy = self.read_existing_schedule()

                self.log.append({
                    "iteration": len(self.log) + 1,
                    "planned": "read existing schedule",
                    "action": "called read_existing_schedule()",
                    "observed": busy,
                    "stopped": False
                })

                # Check conflicts before generating the plan
                self.check_conflicts(busy["busy_days"])

                self.plan = self._build_plan()

                self.goal["schedule_generated"] = True

                self.log.append({
                    "iteration": len(self.log) + 1,
                    "planned": "generate study plan",
                    "action": "created weekly plan after conflict check",
                    "observed": self.plan,
                    "stopped": True,
                    "stop_reason": "study plan generated"
                })

        return self.plan

    # Build study plan
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


if __name__ == "__main__":

   
    existing_schedule = {
        "busy_days": ["Wednesday", "Friday"]
    }

    agent = StudyPlannerAgent(existing_schedule)

    print("=== GENERATING STUDY PLAN ===")

    plan = agent.run()

    print("\n=== FINAL STUDY PLAN ===")
    print(json.dumps(plan, indent=2))

    print("\n=== FULL ITERATION LOG ===")

    for entry in agent.log:
        print(json.dumps(entry, indent=2))
