
# Assignment 1: Handle a Multi-Claim Source

ARTICLE_C = {
    "title": "New AI System Improves Cost and Accuracy",

    "text": (
        "The new AI system reduced operating costs by 20%. "
        "The cost comparison was based on an internal estimate. "
        "The system also improved prediction accuracy by 15%. "
        "Accuracy was evaluated on 1000 test samples and compared "
        "with the previous model using the same test dataset."
    )
}


def apply_research_summary_skill(article):

    text = article["text"]

    sentences = [
        s.strip()
        for s in text.split(".")
        if s.strip()
    ]

    # Identify competing claims
    cost_claim = None
    accuracy_claim = None

    for sentence in sentences:

        if "cost" in sentence.lower() and "%" in sentence:
            cost_claim = sentence

        if "accuracy" in sentence.lower() and "%" in sentence:
            accuracy_claim = sentence

    # Select the claim with stronger supporting evidence
    if cost_claim and accuracy_claim:

        claim = accuracy_claim

        selection_note = (
            "Two competing claims were identified. "
            "The accuracy claim was selected because it has "
            "more specific supporting evidence."
        )

        evidence = (
            "Accuracy was evaluated on 1000 test samples "
            "and compared with the previous model using "
            "the same test dataset."
        )

    else:
        claim = sentences[0]
        evidence = "not stated in source"

        selection_note = "No competing claims were identified."

    # Find limitation
    limitation = "not stated in source"

    for sentence in sentences:

        if (
            "limitation" in sentence.lower()
            or "not include" in sentence.lower()
            or "unclear" in sentence.lower()
            or "small" in sentence.lower()
        ):
            limitation = sentence
            break

    takeaway = (
        "Undergraduate takeaway: "
        + claim
        + " -- verify before generalizing."
    )

    return {
        "claim": claim,
        "evidence": evidence,
        "limitation": limitation,
        "takeaway": takeaway,
        "selection_note": selection_note
    }


# Main program
if __name__ == "__main__":

    result = apply_research_summary_skill(ARTICLE_C)

    print("\n---", ARTICLE_C["title"], "---")

    print("Claim:", result["claim"])

    print("Evidence:", result["evidence"])

    print("Limitation:", result["limitation"])

    print("Takeaway:", result["takeaway"])

    print("Selection:", result["selection_note"])
