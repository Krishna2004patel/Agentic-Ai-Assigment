
# ---------------- Builder Node ----------------

def builder_node(state):

    state["build_attempts"] += 1

    print("Builder attempt:", state["build_attempts"])

    # Fail according to the configured number of failures
    if state["build_attempts"] <= state["fail_count"]:
        state["build_ok"] = False
    else:
        state["build_ok"] = True
        state["code"] = "app.py generated"

    return state


# ---------------- Other Nodes ----------------

def requirement_node(state):
    state["requirements"] = [
        "user login",
        "event listing",
        "RSVP button"
    ]
    return state


def planner_node(state):
    state["tasks"] = {}

    for req in state["requirements"]:
        state["tasks"][req] = f"task_for({req})"

    return state


def tester_node(state):
    state["tests_passed"] = state.get("build_ok", False)
    return state


def reviewer_node(state):
    state["review_clean"] = state.get("tests_passed", False)
    return state


def human_gate_node(state):
    state["human_signoff"] = state.get("review_clean", False)
    return state


# ---------------- Simulation with Retry ----------------

def simulate(fail_count):

    state = {
        "fail_count": fail_count,
        "build_attempts": 0
    }

    print("\nRequirement node")

    requirement_node(state)

    print("Requirements:", state["requirements"])

    print("\nPlanner node")

    planner_node(state)

    print("Tasks:", state["tasks"])

    print("\nBuilder node")

    # First attempt
    builder_node(state)

    # Allow exactly one retry
    if not state["build_ok"]:

        print("Builder failed. Retrying once...")

        builder_node(state)

    # Check after the retry
    if not state["build_ok"]:

        print("Builder failed twice.")

        print("Escalating to human.")

        return

    print("Builder succeeded.")

    print("\nTester node")

    tester_node(state)

    print("Tests passed:", state["tests_passed"])

    print("\nReviewer node")

    reviewer_node(state)

    print("Review clean:", state["review_clean"])

    print("\nHuman gate node")

    human_gate_node(state)

    print("Human signoff:", state["human_signoff"])


# ---------------- Main ----------------

if __name__ == "__main__":

    print("========== SCENARIO A ==========")

    print("Builder fails once and succeeds on retry")

    simulate(fail_count=1)

    print("\n========== SCENARIO B ==========")

    print("Builder fails twice and escalates")

    simulate(fail_count=2)
