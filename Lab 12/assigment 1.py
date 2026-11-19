class CostControlAgent:

    def __init__(self, budget_threshold=10000):
        self.budget_threshold = budget_threshold
        self.audit_log = []

    def _log(self, step, data):
        self.audit_log.append({
            "step": step,
            "data": data
        })

    def propose_change(
        self,
        action,
        estimated_cost=None,
        finance_approved=False
    ):

        # Reject if cost estimate is missing
        if estimated_cost is None:
            self._log(
                "proposal_rejected",
                {"reason": "Cost estimate is missing"}
            )

            return {
                "rejected": True,
                "reason": "Cost estimate is required."
            }

        # Validate cost
        if (
            not isinstance(estimated_cost, (int, float))
            or isinstance(estimated_cost, bool)
            or estimated_cost < 0
        ):
            self._log(
                "proposal_rejected",
                {"reason": "Invalid cost estimate"}
            )

            return {
                "rejected": True,
                "reason": "Invalid cost estimate."
            }

        # Check budget threshold
        if estimated_cost > self.budget_threshold:

            if not finance_approved:
                self._log(
                    "proposal_rejected",
                    {
                        "reason": "Budget exceeded",
                        "estimated_cost": estimated_cost
                    }
                )

                return {
                    "rejected": True,
                    "reason": "Cost exceeds budget. Finance approval required."
                }

        # Proposal accepted
        request = {
            "action": action,
            "estimated_cost": estimated_cost,
            "budget_threshold": self.budget_threshold,
            "finance_approved": finance_approved,
            "status": "approved_for_review"
        }

        self._log("proposal_accepted", request)

        return request


if __name__ == "__main__":

    agent = CostControlAgent(budget_threshold=10000)

    print("=== Test 1: Cost within budget ===")
    print(
        agent.propose_change(
            action="Upgrade server",
            estimated_cost=5000
        )
    )

    print("\n=== Test 2: Cost exceeds budget ===")
    print(
        agent.propose_change(
            action="Purchase new hardware",
            estimated_cost=15000
        )
    )

    print("\n=== Test 3: Cost exceeds budget with finance approval ===")
    print(
        agent.propose_change(
            action="Purchase new hardware",
            estimated_cost=15000,
            finance_approved=True
        )
    )

    print("\n=== Test 4: Adversarial test - Missing cost estimate ===")
    print(
        agent.propose_change(
            action="Upgrade production system"
        )
    )

    print("\n=== Audit Log ===")
    for entry in agent.audit_log:
        print(entry)