
"""
Lab 10 - Assignment 1
A Second Incident Type
"""

LOGS_PAYMENTS = [
    {"ts": "14:00:00", "level": "INFO",
     "msg": "deploy started: payments-service v2.4.1"},
    {"ts": "14:00:45", "level": "INFO",
     "msg": "deploy completed: payments-service v2.4.1"},
    {"ts": "14:03:10", "level": "WARN",
     "msg": "refund endpoint latency elevated"},
    {"ts": "14:03:40", "level": "ERROR",
     "msg": "refund endpoint: NullPointerException in RefundHandler"},
    {"ts": "14:04:05", "level": "ERROR",
     "msg": "refund endpoint: NullPointerException in RefundHandler"}
]

DEPLOY_PAYMENTS = [
    {
        "ts": "14:00:00",
        "service": "payments-service",
        "version": "v2.4.1",
        "prev_version": "v2.4.0"
    }
]

METRICS_PAYMENTS = {
    "baseline_error_rate": 0.5,
    "current_error_rate": 1.6
}


LOGS_DATABASE = [
    {"ts": "15:00:00", "level": "INFO",
     "msg": "deploy started: database-service v3.2.0"},
    {"ts": "15:00:30", "level": "INFO",
     "msg": "deploy completed: database-service v3.2.0"},
    {"ts": "15:02:10", "level": "WARN",
     "msg": "database connection pool usage reached 85%"},
    {"ts": "15:03:00", "level": "ERROR",
     "msg": "database connection pool exhausted"},
    {"ts": "15:03:20", "level": "ERROR",
     "msg": "database connection timeout"},
    {"ts": "15:03:45", "level": "ERROR",
     "msg": "database connection request rejected"}
]

DEPLOY_DATABASE = [
    {
        "ts": "15:00:00",
        "service": "database-service",
        "version": "v3.2.0",
        "prev_version": "v3.1.9"
    }
]

METRICS_DATABASE = {
    "baseline_error_rate": 1.0,
    "current_error_rate": 8.0
}


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

    return "early_warning"


def find_incident_start(logs):
    for entry in logs:
        if entry["level"] == "ERROR":
            return entry["ts"]

    return None


def correlate_with_recent_changes(logs, deploys, incident_start):
    error_messages = [
        entry["msg"].lower()
        for entry in logs
        if entry["level"] == "ERROR"
    ]

    if any("refund" in msg for msg in error_messages):
        affected_path = "refund endpoint"
    elif any(
        "connection pool" in msg or "database" in msg
        for msg in error_messages
    ):
        affected_path = "database connection pool"
    else:
        affected_path = "unknown"

    for deploy in deploys:
        if (
            incident_start is not None
            and deploy["ts"] < incident_start
        ):
            return {
                "hypothesis": (
                    f"Errors began at {incident_start}, shortly after "
                    f"deployment of {deploy['service']} "
                    f"{deploy['version']}. Errors are concentrated in "
                    f"the {affected_path}. This may indicate a "
                    f"regression introduced by the deployment."
                ),
                "suspect_deploy": deploy,
                "affected_path": affected_path
            }

    return {
        "hypothesis": "No recent deployment correlates with the incident.",
        "suspect_deploy": None,
        "affected_path": affected_path
    }


def diagnose_incident(name, logs, deploys, metrics):
    incident_start = find_incident_start(logs)
    hypothesis = correlate_with_recent_changes(
        logs, deploys, incident_start
    )

    return {
        "incident": name,
        "severity": classify_severity(metrics),
        "incident_start": incident_start,
        "diagnosis": hypothesis["hypothesis"],
        "affected_path": hypothesis["affected_path"],
        "suspect_deploy": hypothesis["suspect_deploy"]
    }


if __name__ == "__main__":

    print("=" * 65)
    print("LAB 10 - ASSIGNMENT 1: A SECOND INCIDENT TYPE")
    print("=" * 65)

    payments = diagnose_incident(
        "Payments Service Deployment Failure",
        LOGS_PAYMENTS,
        DEPLOY_PAYMENTS,
        METRICS_PAYMENTS
    )

    database = diagnose_incident(
        "Database Connection-Pool Exhaustion",
        LOGS_DATABASE,
        DEPLOY_DATABASE,
        METRICS_DATABASE
    )

    print("\n=== INCIDENT 1: PAYMENTS SERVICE ===")
    for key, value in payments.items():
        print(f"{key}: {value}")

    print("\n=== INCIDENT 2: DATABASE CONNECTION POOL ===")
    for key, value in database.items():
        print(f"{key}: {value}")

    print("\n=== INCIDENT COMPARISON ===")
    print("Payments severity:", payments["severity"])
    print("Database severity:", database["severity"])
    print("Payments affected path:", payments["affected_path"])
    print("Database affected path:", database["affected_path"])

    assert payments["severity"] != database["severity"]
    assert payments["affected_path"] != database["affected_path"]

    print("\nSUCCESS: Both incidents have different diagnoses and severity.")
