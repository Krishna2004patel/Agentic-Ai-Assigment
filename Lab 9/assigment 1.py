
"""
Lab 9 - Assignment 1
Add a Directly Contradicting Source
"""

QUESTION = (
    "What are the demonstrated benefits and limitations of "
    "retrieval-augmented generation (RAG) for domain-specific "
    "question answering?"
)

SOURCES = [
    {
        "id": "S1",
        "type": "peer-reviewed paper",
        "date": "2026-02",
        "claim": "RAG reduces hallucination rate by 41% on domain QA "
                 "vs a non-retrieval baseline.",
        "evidence": "200 held-out questions from a medical knowledge base.",
        "limitation": "Small, single-domain evaluation set; may not generalize."
    },
    {
        "id": "S2",
        "type": "vendor engineering blog",
        "date": "2026-04",
        "claim": "RAG improves answer accuracy by 35% in an internal "
                 "support-ticket QA system.",
        "evidence": "Internal A/B test over 10,000 tickets.",
        "limitation": "Internal evaluation; no independent replication reported."
    },
    {
        "id": "S3",
        "type": "independent benchmark report",
        "date": "2026-05",
        "claim": "RAG introduces a measurable latency overhead of "
                 "200-400ms per query.",
        "evidence": "Benchmarked across 5 open-source RAG pipelines.",
        "limitation": "Latency depends on index size; not tested at scale."
    },
    {
        "id": "S4",
        "type": "independent evaluation report",
        "date": "2026-06",
        "claim": "RAG showed no measurable reduction in hallucination "
                 "rate compared with a non-retrieval baseline.",
        "evidence": "A separate evaluation using a different domain "
                    "and test dataset.",
        "limitation": "Dataset size and evaluation methodology may differ "
                      "from the S1 study."
    }
]


def build_evidence_table(sources):
    return sources


def compare(sources):
    agreements = []
    conflicts = []
    gaps = []

    source_map = {source["id"]: source for source in sources}

    s1 = source_map.get("S1")
    s2 = source_map.get("S2")
    s3 = source_map.get("S3")
    s4 = source_map.get("S4")

    if s1 and s2:
        agreements.append(
            "S1 and S2 both report improvements from RAG, "
            "although they measure different outcomes and use different domains."
        )

    if s1 and s4:
        conflicts.append(
            "GENUINE CONFLICT: S1 reports a 41% reduction in hallucination "
            "rate, while S4 reports no measurable reduction. "
            "A plausible reason is that the studies used different "
            "evaluation methodologies, domains, or dataset sizes."
        )

    if s3 and (s1 or s2):
        gaps.append(
            "S3 reports additional query latency, while the accuracy-focused "
            "sources do not measure this performance cost."
        )

    gaps.append(
        "The available sources do not report RAG performance "
        "for non-English languages."
    )

    return {
        "agreements": agreements,
        "conflicts": conflicts,
        "gaps": gaps
    }


def synthesize(evidence_table, comparison):
    summary = []

    for source in evidence_table:
        summary.append(
            f"[{source['id']}] {source['claim']}"
        )

    for agreement in comparison["agreements"]:
        summary.append(f"[Agreement] {agreement}")

    for conflict in comparison["conflicts"]:
        summary.append(f"[Conflict: S1 vs S4] {conflict}")

    for gap in comparison["gaps"]:
        summary.append(f"[Research gap] {gap}")

    return summary


if __name__ == "__main__":
    print("=" * 70)
    print("LAB 9 - ASSIGNMENT 1: DIRECTLY CONTRADICTING SOURCE")
    print("=" * 70)

    print("\n=== Research Question ===")
    print(QUESTION)

    table = build_evidence_table(SOURCES)

    print("\n=== Evidence Table ===")
    for source in table:
        print(f"\nSource ID: {source['id']}")
        print(f"Type: {source['type']}")
        print(f"Date: {source['date']}")
        print(f"Claim: {source['claim']}")
        print(f"Evidence: {source['evidence']}")
        print(f"Limitation: {source['limitation']}")

    comparison = compare(table)

    print("\n=== Comparison ===")

    print("\nAgreements:")
    for item in comparison["agreements"]:
        print("-", item)

    print("\nGenuine Conflicts:")
    for item in comparison["conflicts"]:
        print("-", item)

    print("\nResearch Gaps:")
    for item in comparison["gaps"]:
        print("-", item)

    summary = synthesize(table, comparison)

    print("\n=== Executive Summary ===")
    for line in summary:
        print("-", line)

    print("\n=== Recommended Next Questions ===")
    print("- Why did S1 and S4 obtain different hallucination results?")
    print("- Would both studies reach similar results using the same dataset?")
    print("- How does RAG latency change with larger retrieval indexes?")
