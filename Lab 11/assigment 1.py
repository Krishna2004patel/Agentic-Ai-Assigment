
"""
Lab 11 - Assignment 1
A Second, Concurrent Story

Two stories:
US-1: CSV export
US-2: PDF export

Each artifact is attributed to its correct story.
"""


FEATURE_REQUESTS = [
    "Add CSV export to the reports page, preserving applied filters.",
    "Add PDF export to the reports page, preserving applied filters."
]


def requirement_agent(requests):
    stories = [
        {
            "id": "US-1",
            "format": "CSV",
            "text": requests[0],
            "acceptance_criteria": [
                "export produces CSV content",
                "only rows matching applied filters are included",
                "CSV header matches visible column names"
            ]
        },
        {
            "id": "US-2",
            "format": "PDF",
            "text": requests[1],
            "acceptance_criteria": [
                "export produces PDF export content",
                "only rows matching applied filters are included",
                "export contains the visible column names"
            ]
        }
    ]

    return stories


def human_confirms_stories(stories):
    print("[HUMAN CHECKPOINT] Confirming both user stories...")

    for story in stories:
        print(f" Confirmed {story['id']}: {story['text']}")

    return True


def design_agent(stories):
    designs = {}

    for story in stories:
        designs[story["id"]] = {
            "story_id": story["id"],
            "format": story["format"],
            "components": [
                "export_endpoint",
                f"{story['format'].lower()}_serializer",
                "export_button"
            ]
        }

    return designs


def coding_agent(designs, stories):
    implementations = {}

    for story in stories:
        story_id = story["id"]
        export_format = story["format"]

        def export_endpoint(
            rows,
            applied_filters,
            columns,
            selected_format=export_format
        ):
            filtered_rows = [
                row for row in rows
                if all(
                    row.get(key) == value
                    for key, value in applied_filters.items()
                )
            ]

            if selected_format == "CSV":
                lines = [",".join(columns)]

                for row in filtered_rows:
                    lines.append(
                        ",".join(
                            str(row.get(column, ""))
                            for column in columns
                        )
                    )

                return "\n".join(lines)

            # Simulated PDF export content for this offline exercise.
            lines = [
                "PDF EXPORT",
                " | ".join(columns)
            ]

            for row in filtered_rows:
                lines.append(
                    " | ".join(
                        str(row.get(column, ""))
                        for column in columns
                    )
                )

            return "\n".join(lines)

        implementations[story_id] = {
            "story_id": story_id,
            "format": export_format,
            "design_ref": designs[story_id]["components"],
            "export_endpoint": export_endpoint
        }

    return implementations


def testing_agent(stories):
    """
    Test definitions are created from stories only.
    This function does not receive implementation code.
    """

    test_suites = {}

    for story in stories:
        story_id = story["id"]
        export_format = story["format"]
        criteria = story["acceptance_criteria"]

        def test_suite(export_fn, fmt=export_format):
            rows = [
                {"region": "North", "sales": 100},
                {"region": "South", "sales": 200},
                {"region": "North", "sales": 150}
            ]

            columns = ["region", "sales"]

            output = export_fn(
                rows,
                {"region": "North"},
                columns
            )

            results = []

            if fmt == "CSV":
                results.append((
                    "produces CSV content",
                    output.startswith("region,sales")
                ))
            else:
                results.append((
                    "produces PDF export content",
                    output.startswith("PDF EXPORT")
                ))

            results.append((
                "only filtered rows are included",
                all(
                    "South" not in line
                    for line in output.splitlines()
                )
            ))

            results.append((
                "visible column names are included",
                "region" in output and "sales" in output
            ))

            return results, criteria

        test_suites[story_id] = test_suite

    return test_suites


def review_agent(designs, implementations, all_test_results):
    review = {}

    for story_id in designs:
        issues = []

        if len(designs[story_id]["components"]) < 2:
            issues.append("Design has insufficient components.")

        if not all(
            passed
            for _, passed in all_test_results[story_id]
        ):
            issues.append("One or more tests failed.")

        if implementations[story_id]["story_id"] != story_id:
            issues.append("Implementation story ID mismatch.")

        review[story_id] = {
            "story_id": story_id,
            "issues": issues,
            "clean": len(issues) == 0
        }

    return review


def human_final_decision(review):
    print("\n[HUMAN CHECKPOINT] Reviewing both stories...")

    for story_id, result in review.items():
        print(
            f" {story_id}: "
            f"{'accept' if result['clean'] else 'reject'}"
        )

    return all(result["clean"] for result in review.values())


def docs_agent(stories):
    documentation = {}

    for story in stories:
        documentation[story["id"]] = (
            f"Usage: select {story['format']} Export on the reports page "
            f"to export the filtered report. ({story['id']})"
        )

    return documentation


def release_agent(decision, stories):
    releases = {}

    for story in stories:
        story_id = story["id"]

        if not decision:
            releases[story_id] = {
                "released": False,
                "reason": "Human review rejected the release."
            }
        else:
            releases[story_id] = {
                "released": True,
                "release_note": (
                    f"Added {story['format']} export ({story_id})."
                ),
                "rollback_plan": (
                    "Revert the reports-page build if export errors "
                    "increase after release."
                )
            }

    return releases


if __name__ == "__main__":

    stories = requirement_agent(FEATURE_REQUESTS)
    human_confirms_stories(stories)

    designs = design_agent(stories)
    implementations = coding_agent(designs, stories)

    # Test suites are generated from stories, not implementations.
    test_suites = testing_agent(stories)

    all_test_results = {}

    print("\n=== INDEPENDENT TEST RESULTS ===")

    for story in stories:
        story_id = story["id"]

        results, criteria = test_suites[story_id](
            implementations[story_id]["export_endpoint"]
        )

        all_test_results[story_id] = results

        print(f"\n{story_id} - {story['format']} export")
        print("Acceptance criteria:", criteria)

        for name, passed in results:
            print(f" [{'PASS' if passed else 'FAIL'}] {name}")

    review = review_agent(
        designs,
        implementations,
        all_test_results
    )

    print("\n=== REVIEW ===")
    for story_id, result in review.items():
        print(f"{story_id}: {result}")

    decision = human_final_decision(review)

    documentation = docs_agent(stories)
    releases = release_agent(decision, stories)

    print("\n=== DOCUMENTATION ===")
    for story_id, doc in documentation.items():
        print(f"{story_id}: {doc}")

    print("\n=== RELEASE ===")
    for story_id, release in releases.items():
        print(f"{story_id}: {release}")

    print("\n=== LINEAGE TRACE ===")

    for story in stories:
        story_id = story["id"]

        print(f"\n{story_id}:")
        print(f" story <- requirement_agent(request)")
        print(f" design <- design_agent(story {story_id})")
        print(f" code <- coding_agent(design {story_id}, story {story_id})")
        print(f" tests <- testing_agent(story {story_id}) [independent]")
        print(f" review <- review_agent(artifacts {story_id})")
        print(f" docs <- docs_agent(story {story_id})")
        print(f" release <- release_agent(decision, story {story_id})")

    assert set(designs) == {"US-1", "US-2"}
    assert set(implementations) == {"US-1", "US-2"}
    assert set(test_suites) == {"US-1", "US-2"}

    print("\nSUCCESS: Both stories were processed independently.")
