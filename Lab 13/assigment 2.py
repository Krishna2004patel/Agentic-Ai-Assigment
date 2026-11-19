"""
Lab 13 - Assignment 2
Escalate on a Trend, Not Just a Threshold
Mechanical Predictive Maintenance Agent
"""

# Modified sensor log
# All readings remain below the ALARM threshold
SENSOR_LOG = [
    {"t": 0, "vibration_mm_s": 1.8, "temp_c": 60},
    {"t": 1, "vibration_mm_s": 2.9, "temp_c": 65},
    {"t": 2, "vibration_mm_s": 3.1, "temp_c": 67},
    {"t": 3, "vibration_mm_s": 3.4, "temp_c": 69},
    {"t": 4, "vibration_mm_s": 3.6, "temp_c": 70},
]

THRESHOLDS = {
    "vibration_warn": 2.8,
    "vibration_alarm": 4.5,
    "temp_warn": 70,
    "temp_alarm": 80
}


def read_sensor_log():
    return SENSOR_LOG


def classify_condition(reading):

    if (
        reading["vibration_mm_s"] >= THRESHOLDS["vibration_alarm"]
        or reading["temp_c"] >= THRESHOLDS["temp_alarm"]
    ):
        return "ALARM"

    if (
        reading["vibration_mm_s"] >= THRESHOLDS["vibration_warn"]
        or reading["temp_c"] >= THRESHOLDS["temp_warn"]
    ):
        return "WARNING"

    return "NORMAL"


def safety_check(condition):

    if condition == "ALARM":
        return {
            "recommended_action": "recommend_shutdown_for_human_review",
            "auto_execute": False
        }

    if condition == "WARNING":
        return {
            "recommended_action": "schedule_inspection",
            "auto_execute": False
        }

    return {
        "recommended_action": "continue_monitoring",
        "auto_execute": True
    }


def predictive_maintenance_agent():

    log = read_sensor_log()

    # Classify every sensor reading
    conditions = [
        classify_condition(reading)
        for reading in log
    ]

    # Count consecutive WARNING readings at the end of the log
    consecutive_warnings = 0

    for condition in reversed(conditions):

        if condition == "WARNING":
            consecutive_warnings += 1
        else:
            break

    latest = log[-1]

    latest_condition = conditions[-1]

    # Check for three consecutive WARNING readings
    if consecutive_warnings >= 3:

        recommendation = {
            "recommended_action": "schedule_inspection",
            "auto_execute": False
        }

    else:

        recommendation = safety_check(latest_condition)

    result = {
        "domain": "Mechanical Engineering - Predictive Maintenance",
        "latest_reading": latest,
        "latest_condition": latest_condition,
        "consecutive_warnings": consecutive_warnings,
        "recommended_action": recommendation["recommended_action"],
        "auto_executed": recommendation["auto_execute"]
    }

    return result


if __name__ == "__main__":

    result = predictive_maintenance_agent()

    print("=== Trend-Based Predictive Maintenance Agent ===")

    for key, value in result.items():
        print(f"{key}: {value}")

    # Confirm that three consecutive warnings trigger inspection
    assert result["consecutive_warnings"] >= 3

    assert (
        result["recommended_action"] == "schedule_inspection"
    )

    # Confirm no ALARM-level shutdown is auto-executed
    assert result["auto_executed"] is False

    print(
        "\nConfirmed: Three consecutive WARNING readings "
        "trigger inspection."
    )

    print(
        "Confirmed: No automatic shutdown is executed."
    )