
"""
Lab 9 - Assignment 2
Weight Sources by Quality
"""

QUESTION = (
    "What are the demonstrated benefits and limitations of "
    "retrieval-augmented generation (RAG) for domain-specific "
    "question answering?"
)

QUALITY_RANK = {
    "peer-reviewed": 3,
    "independent benchmark": 2,
    "vendor blog": 1
}

SOURCES = [
    {
        "id": "S1",
        "type": "peer-reviewed paper",
        "quality_tier": "peer-reviewed",
        "date": "2026-02",
        "claim": "RAG reduces hallucination rate by 41% on domain QA "
                 "vs a non-retrieval baseline.",
        "evidence": "200 held-out questions from a medical knowledge base.",
        "limitation": "Small, single-domain evaluation set; may not generalize."
    },
    {
        "id": "S2",
        "type": "vendor engineering blog",
        "quality_tier": "vendor blog",
        "date": "2026-04",
        "claim": "RAG improves answer accuracy by 35% in an internal "
                 "support-ticket QA system.",
        "evidence": "Internal A/B test over 10,000 tickets.",
        "limitation": "Internal evaluation; no independent replication reported."
    },
    {
        "id": "S3",
        "type": "independent benchmark report",
        "quality_tier": "independent benchmark",
        "date": "2026-05",
        "claim": "RAG introduces a measurable latency overhead of "
                 "200-400ms per query.",
        "evidence": "Benchmarked across 5 open-source RAG pipelines.",
        "limitation": "Latency depends on index size; not tested at scale."
    },
    {
        "id": "S4",
        "type": "vendor engineering blog",
        "quality_tier": "vendor blog",
        "date": "2026-06",
        "claim": "RAG showed no measurable reduction in hallucination "
                 "rate compared with a non-retrieval baseline.",
        "evidence": "A separate evaluation using a different domain "
                    "and test dataset.",
        "limitation": "Internal evaluation; methodology and dataset "
                      "may differ from S1."
    }
]


def build_evidence_table(sources):
    return sources


def compare(sources):
    source_map = {source["id"]: source for source in sources}

    agreements = []
    conflicts = []
    gaps = []

    s1 = source_map.get("S1")
    s2 = source_map.get("S2")
    s3 = source_map.get("S3")
    s4 = source_map.get("S4")

    if s1 and s2:
        agreements.append(
            "S1 and S2 report improvements from RAG, "
            "although they measure different outcomes."
        )

    if s1 and s4:
        conflicts.append({
            "source_a": s1,
            "source_b": s4,
            "description": (
                "S1 reports a 41% reduction in hallucination rate, "
                "while S4 reports no measurable reduction."
            ),
            "possible_reason": (
                "The studies may use different evaluation methods, "
                "domains, or dataset sizes."
            )
        })

    if s3:
        gaps.append(
            "The accuracy-focused sources do not measure "
            "the latency overhead reported by S3."
        )

    gaps.append(
        "No source reports RAG performance for non-English languages."
    )

    return {
        "agreements": agreements,
        "conflicts": conflicts,
        "gaps": gaps
    }


def select_higher_quality_source(source_a, source_b):
    rank_a = QUALITY_RANK[source_a["quality_tier"]]
    rank_b = QUALITY_RANK[source_b["quality_tier"]]

    if rank_a > rank_b:
        return source_a, source_b

    if rank_b > rank_a:
        return source_b, source_a

    return None, None


def synthesize(evidence_table, comparison):
    summary = []

    summary.append("SOURCE CLAIMS:")

    for source in evidence_table:
        summary.append(
            f"[{source['id']}] ({source['quality_tier']}) "
            f"{source['claim']}"
        )

    summary.append("\nSOURCE QUALITY COMPARISON:")

    for conflict in comparison["conflicts"]:
        source_a = conflict["source_a"]
        source_b = conflict["source_b"]

        preferred, down_weighted = select_higher_quality_source(
            source_a, source_b
        )

        if preferred is None:
            summary.append(
                f"[{source_a['id']}, {source_b['id']}] "
                "Both sources have the same quality tier. "
                "Neither claim is automatically preferred."
            )
        else:
            summary.append(
                f"[{preferred['id']}] The synthesis leans toward this claim "
                f"because its quality tier is "
                f"'{preferred['quality_tier']}', which ranks higher."
            )

            summary.append(
                f"[{down_weighted['id']}] This conflicting claim is "
                f"down-weighted because its quality tier is "
                f"'{down_weighted['quality_tier']}'. "
                "It is disclosed, not discarded."
            )

        summary.append(
            "Reason for disagreement: " + conflict["possible_reason"]
        )

    summary.append("\nAGREEMENTS:")

    for agreement in comparison["agreements"]:
        summary.append("- " + agreement)

    summary.append("\nRESEARCH GAPS:")

    for gap in comparison["gaps"]:
        summary.append("- " + gap)

    return summary


if __name__ == "__main__":
    print("=" * 70)
    print("LAB 9 - ASSIGNMENT 2: WEIGHT SOURCES BY QUALITY")
    print("=" * 70)

    print("\n=== Research Question ===")
    print(QUESTION)

    table = build_evidence_table(SOURCES)

    print("\n=== Evidence Table ===")

    for source in table:
        print(f"\nSource ID: {source['id']}")
        print(f"Type: {source['type']}")
        print(f"Quality Tier: {source['quality_tier']}")
        print(f"Date: {source['date']}")
        print(f"Claim: {source['claim']}")
        print(f"Evidence: {source['evidence']}")
        print(f"Limitation: {source['limitation']}")

    comparison = compare(table)

    print("\n=== Comparison ===")

    print("\nAgreements:")
    for item in comparison["agreements"]:
        print("-", item)

    print("\nConflicts:")
    for item in comparison["conflicts"]:
        print(
            f"- {item['source_a']['id']} vs "
            f"{item['source_b']['id']}: {item['description']}"
        )

    print("\nResearch Gaps:")
    for item in comparison["gaps"]:
        print("-", item)

    summary = synthesize(table, comparison)

    print("\n=== Quality-Weighted Executive Synthesis ===")

    for line in summary:
        print(line)

    print("\n=== Quality Ranking Used ===")
    for tier, rank in sorted(
        QUALITY_RANK.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"{rank}. {tier}")
