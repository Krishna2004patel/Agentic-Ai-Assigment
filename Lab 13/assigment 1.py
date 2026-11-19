"""
Lab 13 - Assignment 1
Electrical Engineering: Electrical Load Forecasting
"""

# Simulated electrical power consumption readings
POWER_LOG = [
    {"t": 0, "load_kw": 45},
    {"t": 1, "load_kw": 50},
    {"t": 2, "load_kw": 58},
    {"t": 3, "load_kw": 65},
    {"t": 4, "load_kw": 78},
    {"t": 5, "load_kw": 92},
]

# Load thresholds
THRESHOLDS = {
    "load_warn": 70,
    "load_alarm": 85
}


def read_power_log():
    return POWER_LOG


def classify_load(reading):

    if reading["load_kw"] >= THRESHOLDS["load_alarm"]:
        return "ALARM"

    if reading["load_kw"] >= THRESHOLDS["load_warn"]:
        return "WARNING"

    return "NORMAL"


def check_load_trend(log):

    if len(log) < 2:
        return "insufficient_data"

    increasing = all(
        log[i + 1]["load_kw"] >= log[i]["load_kw"]
        for i in range(len(log) - 1)
    )

    if increasing:
        return "increasing"

    return "mixed"


def electrical_safety_check(condition):

    if condition == "ALARM":
        return {
            "recommended_action": "disconnect_load_for_human_review",
            "auto_execute": False
        }

    if condition == "WARNING":
        return {
            "recommended_action": "schedule_electrical_inspection",
            "auto_execute": False
        }

    return {
        "recommended_action": "continue_monitoring",
        "auto_execute": True
    }


def electrical_load_agent():

    log = read_power_log()

    latest = log[-1]

    condition = classify_load(latest)

    trend = check_load_trend(log)

    safety = electrical_safety_check(condition)

    result = {
        "domain": "Electrical Engineering - Load Forecasting",
        "latest_reading": latest,
        "condition": condition,
        "trend": trend,
        "recommended_action": safety["recommended_action"],
        "auto_executed": safety["auto_execute"],
        "evaluation_method": (
            "Electrical load threshold classification "
            "with power consumption trend analysis."
        )
    }

    return result


if __name__ == "__main__":

    result = electrical_load_agent()

    print("=== Electrical Load Forecasting Agent ===")

    for key, value in result.items():
        print(f"{key}: {value}")

    # Safety check: ALARM must never be auto-executed
    assert (
        result["condition"] != "ALARM"
        or result["auto_executed"] is False
    ), "ALARM condition requires human review!"

    print(
        "\nConfirmed: ALARM-level electrical actions "
        "require human review."
    )