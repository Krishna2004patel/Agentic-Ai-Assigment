
# Lab 3: Skill Creation
# Research Summary Skill

# Article A: RAG
ARTICLE_A = {
    "title": "Retrieval-Augmented Generation Reduces Hallucination in Domain QA",
    "text": (
        "A recent benchmark study found that retrieval-augmented generation (RAG) "
        "reduced factual hallucination rates by 41% compared to a non-retrieval "
        "baseline on a domain-specific question-answering task. The evaluation used "
        "200 held-out questions from a medical knowledge base. The authors note the "
        "evaluation set was small and drawn from a single domain, so results may not "
        "generalize to other domains without further testing."
    )
}

# Article B: Campus Wi-Fi
ARTICLE_B = {
    "title": "Campus Wi-Fi Upgrade Improves Peak-Hour Throughput",
    "text": (
        "Following a campus-wide Wi-Fi access point upgrade, average peak-hour "
        "throughput in the library increased by 60%. The measurement was taken "
        "over two weeks post-upgrade using the network monitoring dashboard. "
        "The report does not include measurements from other buildings on campus, "
        "so it is unclear whether the improvement is uniform across campus."
    )
}

# Skill instructions and constraints
SKILL_SPEC = {
    "name": "research_summary",

    "instructions": [
        "identify the single main claim",
        "list supporting evidence for that claim",
        "note at least one limitation",
        "write a one-sentence undergraduate-level takeaway"
    ],

    "constraints": [
        "never present a hedged claim as an unhedged fact",
        "never omit the limitation row",
        "use not stated in source if information is absent"
    ]
}


# Function to apply the research summary skill
def apply_research_summary_skill(article):

    text = article["text"]

    sentences = [
        s.strip()
        for s in text.split(".")
        if s.strip()
    ]

    # Extract main claim
    claim = sentences[0]

    # Extract supporting evidence
    if len(sentences) > 1:
        evidence = sentences[1]
    else:
        evidence = "not stated in source"

    # Find limitation
    limitation = "not stated in source"

    for sentence in sentences:

        if (
            "small" in sentence.lower()
            or "does not include" in sentence.lower()
            or "unclear" in sentence.lower()
            or "may not generalize" in sentence.lower()
        ):
            limitation = sentence
            break

    # Generate takeaway
    takeaway = (
        "Undergraduate takeaway: "
        + claim.rstrip(".")
        + " -- but verify before generalizing."
    )

    return {
        "claim": claim,
        "evidence": evidence,
        "limitation": limitation,
        "takeaway": takeaway
    }


# Function to print the summary
def print_skill_output(article, output):

    print("\n---", article["title"], "---")

    print("Claim:", output["claim"])
    print("Evidence:", output["evidence"])
    print("Limitation:", output["limitation"])
    print("Takeaway:", output["takeaway"])


# Check whether the skill works for different articles
def reusability_check(output_a, output_b):

    keys_a = set(output_a.keys())
    keys_b = set(output_b.keys())

    same_structure = keys_a == keys_b

    both_have_limitation = (
        output_a["limitation"] != ""
        and output_b["limitation"] != ""
    )

    print("\n=== Reusability check ===")

    print("Same output structure:", same_structure)

    print(
        "Limitation field populated in both outputs:",
        both_have_limitation
    )

    if same_structure and both_have_limitation:
        print("Conclusion: SKILL IS REUSABLE")
    else:
        print("Conclusion: SKILL NEEDS TIGHTER INSTRUCTIONS")


# Main program
if __name__ == "__main__":

    out_a = apply_research_summary_skill(ARTICLE_A)

    out_b = apply_research_summary_skill(ARTICLE_B)

    print_skill_output(ARTICLE_A, out_a)

    print_skill_output(ARTICLE_B, out_b)

    reusability_check(out_a, out_b)
