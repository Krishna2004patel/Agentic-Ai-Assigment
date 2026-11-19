
from concurrent.futures import ThreadPoolExecutor


# Agent 1: Research
def research_agent(goal):
    return {
        "role": "research",
        "output": "Past events favored a 24-hour format with themed tracks."
    }


# Agent 2: Logistics
def logistics_agent(goal):
    return {
        "role": "logistics",
        "output": {
            "venue": "Grand Hall",
            "venue_cost": 45000,
            "date": "Saturday"
        }
    }


# Agent 3: Budget
def budget_agent(goal):
    return {
        "role": "budget",
        "output": {
            "total_cap": 30000
        }
    }


# Agent 4: Judging
def judging_agent(goal):
    return {
        "role": "judging",
        "output": "Judge on innovation, technical depth, and demo quality."
    }


# Store all agents
ROLES = {
    "research": research_agent,
    "logistics": logistics_agent,
    "budget": budget_agent,
    "judging": judging_agent
}


# Run all agents in parallel
def run_swarm(goal):

    with ThreadPoolExecutor(max_workers=len(ROLES)) as pool:

        futures = {}

        for name, function in ROLES.items():
            futures[name] = pool.submit(function, goal)

        outputs = {}

        for name, future in futures.items():
            outputs[name] = future.result()

    return outputs


# Merge all agent outputs
def merge(outputs):

    draft = {
        "format_notes": outputs["research"]["output"],
        "venue": outputs["logistics"]["output"]["venue"],
        "venue_cost": outputs["logistics"]["output"]["venue_cost"],
        "date": outputs["logistics"]["output"]["date"],
        "budget_cap": outputs["budget"]["output"]["total_cap"],
        "judging_criteria": outputs["judging"]["output"]
    }

    return draft


# Find conflicts
def critique(draft):

    conflicts = []

    if draft["venue_cost"] > draft["budget_cap"]:

        conflicts.append({
            "conflict": "venue_cost exceeds budget_cap",
            "roles_involved": ["logistics", "budget"],
            "logistics_value": draft["venue_cost"],
            "budget_value": draft["budget_cap"]
        })

    return conflicts


# Resolve conflicts
def resolve(conflict, priority_rule="budget_over_preference"):

    if conflict["conflict"] == "venue_cost exceeds budget_cap":

        return {
            "rule_applied": priority_rule,
            "resolution": (
                f"Reject venue at {conflict['logistics_value']}; "
                f"request logistics propose an alternative under "
                f"{conflict['budget_value']}."
            )
        }

    return {
        "rule_applied": priority_rule,
        "resolution": "No rule matched"
    }


# Main program
if __name__ == "__main__":

    outputs = run_swarm("Plan a college AI hackathon")

    print("=== Parallel role outputs ===")

    for name, output in outputs.items():
        print(name, ":", output["output"])

    draft = merge(outputs)

    print("\n=== Merged draft plan ===")
    print(draft)

    conflicts = critique(draft)

    print("\n=== Critique: conflicts found ===")

    conflict_log = []

    for conflict in conflicts:

        resolution = resolve(conflict)

        conflict_log.append({
            **conflict,
            **resolution
        })

        print(conflict)
        print("Resolution:", resolution)

    if not conflicts:
        print("No conflicts found")

    print("\n=== Final conflict log ===")

    for entry in conflict_log:
        print(entry)
