
"""
Lab 10 - Assignment 2
A Safe Auto-Remediation Path
"""

LOGS_WARNING = [
    {"ts": "16:00:00", "level": "INFO",
     "msg": "payments-service is running"},
    {"ts": "16:02:00", "level": "WARN",
     "msg": "one application pod is responding slowly"},
    {"ts": "16:02:30", "level": "WARN",
     "msg": "pod response time exceeded normal threshold"}
]

LOGS_ROLLBACK = [
    {"ts": "17:00:00", "level": "INFO",
     "msg": "deploy started: payments-service v2.5.0"},
    {"ts": "17:01:00", "level": "INFO",
     "msg": "deploy completed: payments-service v2.5.0"},
    {"ts": "17:03:00", "level": "ERROR",
     "msg": "payments-service database transaction failure"},
    {"ts": "17:03:30", "level": "ERROR",
     "msg": "payments-service request processing failure"}
]

METRICS_WARNING = {
    "baseline_error_rate": 1.0,
    "current_error_rate": 1.2
}

METRICS_ROLLBACK = {
    "baseline_error_rate": 0.5,
    "current_error_rate": 4.0
}

DEPLOY_HISTORY = [
    {
        "ts": "17:00:00",
        "service": "payments-service",
        "version": "v2.5.0",
        "prev_version": "v2.4.9"
    }
]


def classify_severity(metrics):
    baseline = metrics["baseline_error_rate"]
    current = metrics["current_error_rate"]

    if baseline <= 0:
        raise ValueError("Baseline error rate must be greater than zero.")

    ratio = current / baseline

    if current > 50:
        return "down"
    if ratio >= 5:
        return "critical"
    if ratio >= 2:
        return "degraded"

    return "warning"


def find_incident_start(logs):
    for entry in logs:
        if entry["level"] == "ERROR":
            return entry["ts"]

    for entry in logs:
        if entry["level"] == "WARN":
            return entry["ts"]

    return None


def correlate_with_recent_changes(logs, deploys, incident_start):
    errors = [
        entry["msg"].lower()
        for entry in logs
        if entry["level"] == "ERROR"
    ]

    warnings = [
        entry["msg"].lower()
        for entry in logs
        if entry["level"] == "WARN"
    ]

    if any("database" in msg for msg in errors):
        affected_path = "database transactions"
    elif any("pod" in msg for msg in warnings):
        affected_path = "application pod"
    else:
        affected_path = "unknown"

    for deploy in deploys:
        if (
            incident_start is not None
            and deploy["ts"] < incident_start
        ):
            return {
                "hypothesis": (
                    f"The incident started at {incident_start}, "
                    f"after deployment of {deploy['service']} "
                    f"{deploy['version']}. The affected area is "
                    f"{affected_path}."
                ),
                "suspect_deploy": deploy,
                "affected_path": affected_path
            }

    return {
        "hypothesis": (
            f"The incident affects {affected_path}. "
            "No related recent deployment was identified."
        ),
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


def execute_low_risk_action(action):
    if risk_level(action) != "low":
        raise PermissionError(
            "Only low-risk actions can execute automatically."
        )

    return {
        "action_executed": action,
        "execution_status": "SUCCESS",
        "message": "Low-risk action executed automatically."
    }


def draft_approval_request(hypothesis, action, rollback_plan):
    return {
        "diagnosis": hypothesis["hypothesis"],
        "proposed_action": action,
        "risk_level": "high",
        "rollback_plan": rollback_plan,
        "status": "AWAITING HUMAN APPROVAL - NOT EXECUTED"
    }


def diagnose_and_propose(
    logs,
    deploys,
    metrics,
    proposed_action
):
    severity = classify_severity(metrics)
    incident_start = find_incident_start(logs)

    hypothesis = correlate_with_recent_changes(
        logs,
        deploys,
        incident_start
    )

    risk = risk_level(proposed_action)

    if risk == "low":
        execution = execute_low_risk_action(proposed_action)

        return {
            "severity": severity,
            "incident_start": incident_start,
            "diagnosis": hypothesis["hypothesis"],
            "proposed_action": proposed_action,
            "risk": risk,
            **execution
        }

    if risk == "high":
        suspect = hypothesis["suspect_deploy"]

        if suspect:
            rollback_plan = (
                f"Revert to {suspect['prev_version']}; "
                "if problems continue, investigate before "
                "another deployment."
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

        return {
            "severity": severity,
            "incident_start": incident_start,
            **request
        }

    return {
        "severity": severity,
        "diagnosis": hypothesis["hypothesis"],
        "proposed_action": proposed_action,
        "status": "REJECTED - UNKNOWN ACTION RISK"
    }


if __name__ == "__main__":

    print("=" * 65)
    print("LAB 10 - ASSIGNMENT 2: SAFE AUTO-REMEDIATION")
    print("=" * 65)

    print("\n=== SCENARIO 1: WARNING-LEVEL INCIDENT ===")

    warning_result = diagnose_and_propose(
        LOGS_WARNING,
        [],
        METRICS_WARNING,
        "restart_single_pod"
    )

    for key, value in warning_result.items():
        print(f"{key}: {value}")

    print("\n=== SCENARIO 2: HIGH-RISK ROLLBACK ===")

    rollback_result = diagnose_and_propose(
        LOGS_ROLLBACK,
        DEPLOY_HISTORY,
        METRICS_ROLLBACK,
        "rollback"
    )

    for key, value in rollback_result.items():
        print(f"{key}: {value}")

    print("\n=== SAFETY VERIFICATION ===")

    assert (
        warning_result.get("action_executed")
        == "restart_single_pod"
    ), "Low-risk action should execute automatically."

    assert (
        rollback_result.get("status")
        == "AWAITING HUMAN APPROVAL - NOT EXECUTED"
    ), "Rollback must require human approval."

    assert (
        "action_executed" not in rollback_result
    ), "High-risk rollback must never execute automatically."

    print("PASS: Low-risk action executed automatically.")
    print("PASS: High-risk rollback requires human approval.")
    print("PASS: No high-risk action was executed automatically.")

    print("\nAll safety checks passed.")
