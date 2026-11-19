
"""
Lab 11 - Assignment 2
Prove Test Independence With a Deliberate Bug

The coding agent contains an intentional filter bug.
The testing agent remains unchanged and independent.
"""


FEATURE_REQUEST = (
    "Add CSV export to the reports page, preserving applied filters."
)


def requirement_agent(request):
    return [{
        "id": "US-1",
        "text": (
            "As a user, I can export the current report view as a CSV file, "
            "preserving the applied filters."
        ),
        "acceptance_criteria": [
            "clicking Export produces a .csv file",
            "the CSV contains only rows matching the currently applied filters",
            "the CSV header row matches the visible column names"
        ]
    }]


def design_agent(stories):
    return {
        "story_id": stories[0]["id"],
        "components": [
            "export_endpoint",
            "csv_serializer",
            "export_button"
        ]
    }


def coding_agent(design, stories):
    """
    INTENTIONAL BUG:
    Uses != instead of == when applying filters.
    This selects rows that do NOT match the filter.
    """

    def export_endpoint(rows, applied_filters, columns):

        # Deliberate incorrect comparison for assignment demonstration.
        filtered = [
            row for row in rows
            if all(
                row.get(key) != value
                for key, value in applied_filters.items()
            )
        ]

        lines = [",".join(columns)]

        for row in filtered:
            lines.append(
                ",".join(str(row.get(column, "")) for column in columns)
            )

        return "\n".join(lines)

    return {
        "story_id": stories[0]["id"],
        "design_ref": design["components"],
        "export_endpoint": export_endpoint
    }


def testing_agent(stories):
    """
    Tests are generated only from the user story.
    The implementation is not received or inspected here.
    """

    acceptance_criteria = stories[0]["acceptance_criteria"]

    def test_suite(export_fn):
        rows = [
            {"region": "North", "sales": 100},
            {"region": "South", "sales": 200},
            {"region": "North", "sales": 150}
        ]

        columns = ["region", "sales"]

        csv_output = export_fn(
            rows,
            {"region": "North"},
            columns
        )

        results = []

        results.append((
            "produces output",
            len(csv_output) > 0
        ))

        results.append((
            "header matches columns",
            csv_output.splitlines()[0] == "region,sales"
        ))

        results.append((
            "only filtered rows present",
            all(
                "South" not in line
                for line in csv_output.splitlines()[1:]
            )
        ))

        return results, acceptance_criteria, csv_output

    return test_suite


def review_agent(design, code, test_results):
    issues = []

    if len(code["design_ref"]) < 2:
        issues.append("Design has fewer than 2 components.")

    if not all(passed for _, passed in test_results):
        issues.append("One or more independent tests failed.")

    return {
        "story_id": code["story_id"],
        "issues": issues,
        "clean": len(issues) == 0
    }


if __name__ == "__main__":

    print("=" * 65)
    print("LAB 11 - ASSIGNMENT 2")
    print("PROVE TEST INDEPENDENCE WITH A DELIBERATE BUG")
    print("=" * 65)

    stories = requirement_agent(FEATURE_REQUEST)

    print("\n=== REQUIREMENT ===")
    print(stories)

    design = design_agent(stories)

    # Test suite is created before implementation is supplied.
    test_suite = testing_agent(stories)

    print("\nTesting agent created tests from acceptance criteria.")
    print("Testing agent did not receive implementation code.")

    code = coding_agent(design, stories)

    # Run the independently-created tests against the implementation.
    test_results, criteria, csv_output = test_suite(
        code["export_endpoint"]
    )

    print("\n=== IMPLEMENTATION OUTPUT ===")
    print(csv_output)

    print("\n=== INDEPENDENT TEST RESULTS ===")
    print("Acceptance criteria:", criteria)

    for name, passed in test_results:
        status = "PASS" if passed else "FAIL"
        print(f" [{status}] {name}")

    review = review_agent(design, code, test_results)

    print("\n=== REVIEW ===")
    print(review)

    print("\n=== LINEAGE ===")
    print("stories <- requirement_agent(feature_request)")
    print("design <- design_agent(stories)")
    print("tests <- testing_agent(stories) [independent of code]")
    print("code <- coding_agent(design, stories)")
    print("test execution <- test_suite(code['export_endpoint'])")
    print("review <- review_agent(design, code, test_results)")

    failed_tests = [
        name for name, passed in test_results if not passed
    ]

    assert failed_tests, (
        "Expected the independent tests to catch the deliberate bug."
    )

    assert not review["clean"], (
        "Review should reject the implementation because a test failed."
    )

    print("\n=== CONCLUSION ===")
    print("PASS: Independent tests detected the deliberate filter bug.")
    print("PASS: Review identified the failed test.")
    print("PASS: The faulty implementation was not accepted.")
