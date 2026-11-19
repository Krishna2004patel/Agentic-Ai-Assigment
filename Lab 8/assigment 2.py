
from concurrent.futures import ThreadPoolExecutor


# Agent functions
def research_agent(goal):
    return {
        "role": "research",
        "output": {
            "format_notes": "24-hour format with themed tracks"
        }
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
        "output": {
            "criteria": "Innovation, technical depth and demo quality"
        }
    }


def marketing_agent(goal):
    return {
        "role": "marketing",
        "output": {
            "publicity_plan": "Social media campaigns and posters",
            "marketing_cost": 12000,
            "marketing_limit": 10000
        }
    }


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


# Merge all results
def merge(outputs):

    draft = {
        "format_notes": outputs["research"]["output"]["format_notes"],
        "venue": outputs["logistics"]["output"]["venue"],
        "venue_cost": outputs["logistics"]["output"]["venue_cost"],
        "date": outputs["logistics"]["output"]["date"],
        "budget_cap": outputs["budget"]["output"]["total_cap"],
        "judging_criteria": outputs["judging"]["output"]["criteria"],
        "publicity_plan": outputs["marketing"]["output"]["publicity_plan"],
        "marketing_cost": outputs["marketing"]["output"]["marketing_cost"],
        "marketing_limit": outputs["marketing"]["output"]["marketing_limit"]
    }

    return draft


# Research agent independently critiques the plan
def research_critique(draft):

    if not draft["format_notes"]:
        return {
            "role": "research",
            "objection": "Hackathon format information is missing"
        }

    return None


# Logistics agent independently critiques the plan
def logistics_critique(draft):

    if draft["venue_cost"] > draft["budget_cap"]:
        return {
            "role": "logistics",
            "objection": "Venue cost exceeds the approved budget",
            "value": draft["venue_cost"]
        }

    return None


# Budget agent independently critiques the plan
def budget_critique(draft):

    total_cost = draft["venue_cost"] + draft["marketing_cost"]

    if total_cost > draft["budget_cap"]:
        return {
            "role": "budget",
            "objection": "Total expenses exceed the overall budget",
            "total_cost": total_cost,
            "budget_cap": draft["budget_cap"]
        }

    return None


# Judging agent independently critiques the plan
def judging_critique(draft):

    if not draft["judging_criteria"]:
        return {
            "role": "judging",
            "objection": "Judging criteria are missing"
        }

    return None


# Marketing agent independently critiques the plan
def marketing_critique(draft):

    if draft["marketing_cost"] > draft["marketing_limit"]:
        return {
            "role": "marketing",
            "objection": "Marketing expenses exceed the marketing limit",
            "marketing_cost": draft["marketing_cost"],
            "marketing_limit": draft["marketing_limit"]
        }

    return None


# Each role has its own critique function
CRITICS = {
    "research": research_critique,
    "logistics": logistics_critique,
    "budget": budget_critique,
    "judging": judging_critique,
    "marketing": marketing_critique
}


# Run all critiques independently
def distributed_critique(draft):

    conflicts = []

    with ThreadPoolExecutor(max_workers=len(CRITICS)) as pool:

        futures = {}

        for role, function in CRITICS.items():
            futures[role] = pool.submit(function, draft)

        for role, future in futures.items():

            result = future.result()

            if result is not None:
                conflicts.append(result)

    return conflicts


# Main program
if __name__ == "__main__":

    outputs = run_swarm("Plan a college AI hackathon")

    print("=== Agent outputs ===")

    for name, output in outputs.items():
        print(name, ":", output["output"])

    draft = merge(outputs)

    print("\n=== Merged draft ===")
    print(draft)

    conflicts = distributed_critique(draft)

    print("\n=== Distributed critique ===")

    for conflict in conflicts:
        print(conflict)

    print("\n=== Conflict log ===")

    for conflict in conflicts:
        print(
            "Raised by:", conflict["role"],
            "| Objection:", conflict["objection"]
        )
