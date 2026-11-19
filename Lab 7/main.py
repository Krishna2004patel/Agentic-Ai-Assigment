
# ---------------- Node Class ----------------

class Node:

    def __init__(self, name, owner, success_fn, on_success, on_fail):
        self.name = name
        self.owner = owner
        self.success_fn = success_fn
        self.on_success = on_success
        self.on_fail = on_fail


# ---------------- Node Functions ----------------

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


def builder_node(state):

    if state.get("force_build_fail"):
        state["build_ok"] = False
        return state

    state["build_ok"] = True
    state["code"] = "app.py generated"

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


# ---------------- Success Check Functions ----------------

def requirement_success(state):
    return len(state.get("requirements", [])) >= 3


def planner_success(state):
    return all(
        req in state.get("tasks", {})
        for req in state.get("requirements", [])
    )


def builder_success(state):
    return state.get("build_ok", False)


def tester_success(state):
    return state.get("tests_passed", False)


def reviewer_success(state):
    return state.get("review_clean", False)


def human_success(state):
    return state.get("human_signoff", False)


# ---------------- Graph Definition ----------------

GRAPH = [

    Node(
        "requirement",
        "requirement_agent",
        requirement_success,
        requirement_node,
        "escalate_to_human"
    ),

    Node(
        "planner",
        "planner_agent",
        planner_success,
        planner_node,
        "return_to_requirement"
    ),

    Node(
        "builder",
        "builder_agent",
        builder_success,
        builder_node,
        "retry_build_or_escalate"
    ),

    Node(
        "tester",
        "tester_agent",
        tester_success,
        tester_node,
        "route_back_to_builder"
    ),

    Node(
        "reviewer",
        "reviewer_agent",
        reviewer_success,
        reviewer_node,
        "route_back_to_builder"
    ),

    Node(
        "human_gate",
        "human",
        human_success,
        human_gate_node,
        "return_to_planner"
    )

]


# ---------------- Simulation ----------------

def simulate(force_build_fail=False):

    state = {
        "force_build_fail": force_build_fail
    }

    trace = []

    for node in GRAPH:

        state = node.on_success(state)

        ok = node.success_fn(state)

        trace.append({
            "node": node.name,
            "owner": node.owner,
            "success": ok,
            "state_after": {
                k: v for k, v in state.items()
                if k != "force_build_fail"
            }
        })

        if not ok:

            trace.append({
                "node": node.name,
                "failure_behavior_triggered": node.on_fail
            })

            break

    return trace


# ---------------- Main Program ----------------

if __name__ == "__main__":

    print("=== SUCCESS PATH ===")

    for step in simulate(force_build_fail=False):
        print(step)

    print("\n=== FAILURE PATH (builder fails) ===")

    for step in simulate(force_build_fail=True):
        print(step)
