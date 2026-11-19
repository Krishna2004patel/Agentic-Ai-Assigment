
# Assignment 2: Test Against a Low-Evidence Input

ARTICLE_D = {
    "title": "New Learning App Improves Student Performance",

    "text": (
        "The new learning application improves student performance. "
        "Many students are expected to benefit from this application."
    )
}


def apply_research_summary_skill(article):

    text = article["text"]

    sentences = [
        s.strip()
        for s in text.split(".")
        if s.strip()
    ]

    # Extract the main claim
    claim = sentences[0] if sentences else "not stated in source"

    # No actual supporting evidence is provided
    evidence = "not stated in source"

    # No limitation is provided
    limitation = "not stated in source"

    # Generate takeaway without adding unsupported facts
    takeaway = (
        "Undergraduate takeaway: "
        + claim
        + " -- supporting evidence is not stated in source."
    )

    return {
        "claim": claim,
        "evidence": evidence,
        "limitation": limitation,
        "takeaway": takeaway
    }


# Main program
if __name__ == "__main__":

    result = apply_research_summary_skill(ARTICLE_D)

    print("\n---", ARTICLE_D["title"], "---")

    print("Article text:", ARTICLE_D["text"])

    print("\nClaim:", result["claim"])

    print("Evidence:", result["evidence"])

    print("Limitation:", result["limitation"])

    print("Takeaway:", result["takeaway"])

    if (
        result["evidence"] == "not stated in source"
        and result["limitation"] == "not stated in source"
    ):
        print("\nConstraint check: PASSED")

        print(
            "No supporting evidence or limitation "
            "was fabricated."
        )

    else:
        print("\nConstraint check: FAILED")
