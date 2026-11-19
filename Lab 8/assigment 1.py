
from concurrent.futures import ThreadPoolExecutor


def research_agent(goal):
    return {
        "role": "research",
        "output": "24-hour hackathon with themed tracks"
    }


def logistics_agent(goal):
    return {
        "role": "logistics",
        "output": {
            "venue": "Grand Hall",
            "venue_cost": 45000,
            "date": "Saturday"
        }
    }


def budget_agent(goal):
    return {
        "role": "budget",
        "output": {
            "total_cap": 30000
        }
    }


def judging_agent(goal):
    return {
        "role": "judging",
        "output": "Innovation, technical depth and demo quality"
    }


# New fifth agent
def marketing_agent(goal):
    return {
        "role": "marketing",
        "output": {
            "publicity_plan": "Social media campaigns and posters",
            "marketing_cost": 12000
        }
    }


# Register all five agents
ROLES = {
    "research": research_agent,
    "logistics": logistics_agent,
    "budget": budget_agent,
    "judging": judging_agent,
    "marketing": marketing_agent
}


# Run agents in parallel
def run_swarm(goal):

    with ThreadPoolExecutor(max_workers=len(ROLES)) as pool:

        futures = {}

        for name, function in ROLES.items():
            futures[name] = pool.submit(function, goal)

        outputs = {}

        for name, future in futures.items():
            outputs[name] = future.result()

    return outputs


# Merge agent outputs
def merge(outputs):

    draft = {
        "format_notes": outputs["research"]["output"],
        "venue": outputs["logistics"]["output"]["venue"],
        "venue_cost": outputs["logistics"]["output"]["venue_cost"],
        "date": outputs["logistics"]["output"]["date"],
        "budget_cap": outputs["budget"]["output"]["total_cap"],
        "judging_criteria": outputs["judging"]["output"],
        "publicity_plan": outputs["marketing"]["output"]["publicity_plan"],
        "marketing_cost": outputs["marketing"]["output"]["marketing_cost"]
    }

    return draft


# Check conflicts
def critique(draft):

    conflicts = []

    total_cost = draft["venue_cost"] + draft["marketing_cost"]

    if draft["venue_cost"] > draft["budget_cap"]:

        conflicts.append({
            "conflict": "venue cost exceeds budget",
            "roles_involved": ["logistics", "budget"],
            "venue_cost": draft["venue_cost"],
            "budget_cap": draft["budget_cap"]
        })

    if total_cost > draft["budget_cap"]:

        conflicts.append({
            "conflict": "marketing and venue expenses exceed overall budget",
            "roles_involved": ["marketing", "logistics", "budget"],
            "marketing_cost": draft["marketing_cost"],
            "venue_cost": draft["venue_cost"],
            "total_cost": total_cost,
            "budget_cap": draft["budget_cap"]
        })

    return conflicts


# Resolve conflicts
def resolve(conflict):

    return {
        "rule_applied": "budget_over_preference",
        "resolution": (
            f"Total planned cost is {conflict['total_cost']}. "
            f"Reduce expenses to stay within budget of "
            f"{conflict['budget_cap']}."
        )
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

    print("\n=== Conflicts found ===")

    conflict_log = []

    for conflict in conflicts:

        resolution = resolve(conflict)

        entry = {
            **conflict,
            **resolution
        }

        conflict_log.append(entry)

        print(entry)

    print("\n=== Extended conflict log ===")

    for entry in conflict_log:
        print(entry)
