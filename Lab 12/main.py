"""
Lab 12: Safety, Evaluation, and Governance
Guardrails for a Production-Change Agent
"""

REGRESSION_SUITE_RESULT = {"passed": 9, "total": 10}


class ProdChangeAgent:
    permissions = {"can_write": "staging_only"}

    def __init__(self):
        self.audit_log = []
        self.evaluated = False

    def evaluate(self):
        pass_rate = (
            REGRESSION_SUITE_RESULT["passed"]
            / REGRESSION_SUITE_RESULT["total"]
        )

        self.evaluated = pass_rate >= 0.8

        self._log(
            "evaluation",
            {
                "pass_rate": pass_rate,
                "passed_gate": self.evaluated
            }
        )

        return self.evaluated

    def _log(self, step, data):
        self.audit_log.append({
            "step": step,
            "data": data
        })

    def propose_change(
        self, diagnosis, action, rollback_plan, privacy_scrubbed
    ):
        if not self.evaluated:
            self._log(
                "propose_change",
                {"rejected": True, "reason": "agent not evaluated"}
            )
            return {
                "rejected": True,
                "reason": "Evaluation gate not passed; cannot propose changes."
            }

        if self.permissions["can_write"] != "staging_only":
            raise PermissionError(
                "Agent must not hold direct production write access."
            )

        if not privacy_scrubbed:
            self._log(
                "propose_change",
                {
                    "rejected": True,
                    "reason": "unscrubbed customer data in input"
                }
            )
            return {
                "rejected": True,
                "reason": "Diagnostic input was not privacy-scrubbed; rejecting."
            }

        if not rollback_plan:
            self._log(
                "propose_change",
                {
                    "rejected": True,
                    "reason": "no rollback plan supplied"
                }
            )
            return {
                "rejected": True,
                "reason": "No rollback plan defined; rejecting proposal."
            }

        request = {
            "diagnosis": diagnosis,
            "proposed_action": action,
            "rollback_plan": rollback_plan,
            "category": "production",
            "requires_approval": True
        }

        self._log("approval_requested", request)
        return request

    def apply_after_approval(self, request, human_decision):
        self._log(
            "human_decision",
            {"decision": human_decision}
        )

        if human_decision != "approved":
            return {
                "applied": False,
                "reason": "not approved by human"
            }

        return {
            "applied": False,
            "handed_off_to": "privileged_deploy_process",
            "note": (
                "This agent never holds production write access; "
                "a separate privileged process performs the actual apply step."
            )
        }


if __name__ == "__main__":
    agent = ProdChangeAgent()

    print("=== Control 2: Evaluation gate ===")
    print("Evaluated and passed:", agent.evaluate())

    print("\n=== Attempt 1: Missing rollback plan ===")
    result = agent.propose_change(
        diagnosis="Config X causes memory leak under load.",
        action="Revert config X to previous value",
        rollback_plan=None,
        privacy_scrubbed=True
    )
    print(result)

    print("\n=== Attempt 2: Unscrubbed customer data ===")
    result = agent.propose_change(
        diagnosis="Config X causes memory leak under load.",
        action="Revert config X to previous value",
        rollback_plan="Revert config X to v3 if v4 also leaks.",
        privacy_scrubbed=False
    )
    print(result)

    print("\n=== Attempt 3: Complete valid proposal ===")
    request = agent.propose_change(
        diagnosis="Config X causes memory leak under load.",
        action="Revert config X to previous value",
        rollback_plan="Revert config X to v3 if v4 also leaks.",
        privacy_scrubbed=True
    )
    print(request)

    print("\n=== Human approval ===")
    outcome = agent.apply_after_approval(
        request,
        human_decision="approved"
    )
    print(outcome)

    print("\n=== Adversarial test: Direct production write ===")
    try:
        agent.permissions["can_write"] = "production"

        agent.propose_change(
            "Test diagnosis",
            "Test action",
            "Test rollback",
            True
        )

    except PermissionError as e:
        print("Blocked as expected:", e)

    print("\n=== Full Audit Log ===")
    for entry in agent.audit_log:
        print(entry)