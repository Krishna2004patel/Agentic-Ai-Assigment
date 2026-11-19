
"""
Lab 10: Cloud Operations Agent
Failed Deployment Diagnosis

Observe -> Reason -> Act
High-risk actions always require human approval.
"""

LOGS = [
    {
        "ts": "14:00:00",
        "level": "INFO",
        "msg": "deploy started: payments-service v2.4.1"
    },
    {
        "ts": "14:00:45",
        "level": "INFO",
        "msg": "deploy completed: payments-service v2.4.1"
    },
    {
        "ts": "14:03:10",
        "level": "WARN",
        "msg": "refund endpoint latency elevated"
    },
    {
        "ts": "14:03:40",
        "level": "ERROR",
        "msg": "refund endpoint: NullPointerException in RefundHandler"
    },
    {
        "ts": "14:04:05",
        "level": "ERROR",
        "msg": "refund endpoint: NullPointerException in RefundHandler"
    },
    {
        "ts": "14:04:30",
        "level": "ERROR",
        "msg": "refund endpoint: NullPointerException in RefundHandler"
    }
]

DEPLOY_HISTORY = [
    {
        "ts": "14:00:00",
        "service": "payments-service",
        "version": "v2.4.1",
        "prev_version": "v2.4.0"
    }
]

METRICS = {
    "baseline_error_rate": 0.5,
    "current_error_rate": 1.6
}


def classify_severity(metrics):
    baseline = metrics["baseline_error_rate"]
    current = metrics["current_error_rate"]

    if baseline <= 0:
        raise ValueError("Baseline error rate must be greater than zero.")

    ratio = current / baseline

    if current > 50:
        return "down"

    if ratio >= 2:
        return "degraded"

    return "early_warning"


def find_incident_start(logs):
    for entry in logs:
        if entry["level"] == "ERROR":
            return entry["ts"]

    return None


def correlate_with_recent_changes(logs, deploys, incident_start):
    error_messages = [
        entry["msg"]
        for entry in logs
        if entry["level"] == "ERROR"
    ]

    affected_path = (
        "refund"
        if any("refund" in msg.lower() for msg in error_messages)
        else "unknown"
    )

    for deploy in deploys:
        if (
            incident_start is not None
            and deploy["ts"] < incident_start
            and deploy["service"].lower().startswith("payments")
        ):
            return {
                "hypothesis": (
                    f"Error rate rose starting {incident_start}, shortly "
                    f"after the {deploy['ts']} deploy of "
                    f"{deploy['service']} {deploy['version']}. "
                    f"Errors are concentrated in the {affected_path} "
                    f"code path, consistent with a regression introduced "
                    f"in that release."
                ),
                "suspect_deploy": deploy,
                "affected_path": affected_path
            }

    return {
        "hypothesis": "No recent deploy correlates with the incident window.",
        "suspect_deploy": None,
        "affected_path": affected_path
    }


def risk_level(action):
    high_risk = {
        "rollback",
        "scale",
        "config_change",
        "delete"
    }

    low_risk = {
        "open_ticket",
        "notify",
        "restart_single_pod"
    }

    if action in high_risk:
        return "high"

    if action in low_risk:
        return "low"

    return "unknown"


def draft_approval_request(hypothesis, action, rollback_plan):
    return {
        "diagnosis": hypothesis["hypothesis"],
        "proposed_action": action,
        "risk_if_wrong": (
            "Brief service interruption (~30 seconds) during rollback "
            "if the hypothesis is incorrect."
        ),
        "rollback_plan": rollback_plan,
        "status": "AWAITING HUMAN APPROVAL -- NOT EXECUTED"
    }


def diagnose_and_propose(
    logs,
    deploys,
    metrics,
    urgency_prompt=False
):
    severity = classify_severity(metrics)

    incident_start = find_incident_start(logs)

    hypothesis = correlate_with_recent_changes(
        logs,
        deploys,
        incident_start
    )

    proposed_action = "rollback"
    risk = risk_level(proposed_action)

    if risk == "high":
        suspect = hypothesis["suspect_deploy"]

        if suspect:
            rollback_plan = (
                f"Revert to {suspect['prev_version']}; "
                f"if that also errors, investigate before "
                f"another deployment."
            )
        else:
            rollback_plan = (
                "Identify and verify the last stable version "
                "before requesting rollback approval."
            )

        request = draft_approval_request(
            hypothesis,
            proposed_action,
            rollback_plan
        )

        if urgency_prompt:
            request["note"] = (
                "Urgency noted, but high-risk action still requires "
                "human approval -- the approval gate is not bypassed."
            )

        return {
            "severity": severity,
            "incident_start": incident_start,
            **request
        }

    if risk == "low":
        return {
            "severity": severity,
            "incident_start": incident_start,
            "diagnosis": hypothesis["hypothesis"],
            "proposed_action": proposed_action,
            "action_executed": proposed_action
        }

    return {
        "severity": severity,
        "incident_start": incident_start,
        "diagnosis": hypothesis["hypothesis"],
        "proposed_action": proposed_action,
        "status": "REJECTED - UNKNOWN ACTION RISK"
    }


if __name__ == "__main__":

    result = diagnose_and_propose(
        LOGS,
        DEPLOY_HISTORY,
        METRICS,
        urgency_prompt=True
    )

    print("=== Diagnostic + Approval Request ===")

    for key, value in result.items():
        print(f"{key}: {value}")

    assert (
        "action_executed" not in result
    ), "High-risk action must never auto-execute!"

    print(
        "\nConfirmed: no destructive action was executed automatically."
    )
