REGRESSION_SUITE_RESULT = {
    "passed": 9,
    "total": 10
}


class ReEvaluationAgent:

    def __init__(self, max_proposals=5):
        self.max_proposals = max_proposals
        self.total_proposals = 0
        self.proposals_since_evaluation = 0
        self.evaluated = False
        self.audit_log = []

    def _log(self, step, data):
        self.audit_log.append({
            "step": step,
            "data": data
        })

    def evaluate(self):

        pass_rate = (
            REGRESSION_SUITE_RESULT["passed"]
            / REGRESSION_SUITE_RESULT["total"]
        )

        self.evaluated = pass_rate >= 0.8

        if self.evaluated:
            self.proposals_since_evaluation = 0

        self._log(
            "evaluation",
            {
                "pass_rate": pass_rate,
                "passed_gate": self.evaluated
            }
        )

        return self.evaluated

    def propose_change(self, action):

        # Check whether evaluation has been completed
        if not self.evaluated:
            message = "Agent must pass evaluation before making proposals."

            self._log(
                "proposal_blocked",
                {"reason": message}
            )

            return {
                "rejected": True,
                "reason": message
            }

        # Block proposal after every 5 proposals
        if self.proposals_since_evaluation >= self.max_proposals:

            message = (
                "Proposal limit reached. "
                "Call evaluate() again before making another proposal."
            )

            self._log(
                "proposal_blocked",
                {"reason": message}
            )

            return {
                "rejected": True,
                "reason": message
            }

        # Accept proposal
        self.total_proposals += 1
        self.proposals_since_evaluation += 1

        request = {
            "action": action,
            "proposal_number": self.total_proposals,
            "status": "accepted"
        }

        self._log("proposal_accepted", request)

        return request


if __name__ == "__main__":

    agent = ReEvaluationAgent(max_proposals=5)

    print("=== Initial Evaluation ===")
    print("Evaluation passed:", agent.evaluate())

    print("\n=== First 5 Proposals ===")

    for i in range(1, 6):
        result = agent.propose_change(
            action=f"Production change {i}"
        )

        print(result)

    print("\n=== 6th Proposal: Should Be Blocked ===")

    result = agent.propose_change(
        action="Production change 6"
    )

    print(result)

    print("\n=== Re-Evaluation ===")

    print("Evaluation passed:", agent.evaluate())

    print("\n=== 6th Proposal After Re-Evaluation ===")

    result = agent.propose_change(
        action="Production change 6"
    )

    print(result)

    print("\n=== Full Audit Log ===")

    for entry in agent.audit_log:
        print(entry)