from .algorithms import (
    insertion_sort,
    binary_search,
    linear_search,
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


def test_insertion_sort():
    # Empty list
    empty = []
    insertion_sort(empty, "id")
    assert empty == []

    # Single element
    single = [{"id": 1}]
    insertion_sort(single, "id")
    assert single == [{"id": 1}]

    # Normal unsorted list
    records = [
        {"id": 3},
        {"id": 1},
        {"id": 2},
    ]

    insertion_sort(records, "id")

    assert records == [
        {"id": 1},
        {"id": 2},
        {"id": 3},
    ]

    print("Insertion Sort: PASS")


def test_binary_search():
    records = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
        {"id": 5},
    ]

    # First element
    assert binary_search(records, 1, "id") == 0

    # Middle element
    assert binary_search(records, 3, "id") == 2

    # Last element
    assert binary_search(records, 5, "id") == 4

    # Not found
    assert binary_search(records, 99, "id") == -1

    print("Binary Search: PASS")


def test_linear_search():
    records = [
        {"id": 10},
        {"id": 20},
        {"id": 30},
    ]

    assert linear_search(records, 10, "id") == 0
    assert linear_search(records, 30, "id") == 2
    assert linear_search(records, 99, "id") == -1

    print("Linear Search: PASS")


def test_insertion_sort_count():
    records = [
        {"id": 3},
        {"id": 2},
        {"id": 1},
    ]

    result = insertion_sort_count(records, "id")

    assert type(result) is int
    assert result > 0

    assert records == [
        {"id": 1},
        {"id": 2},
        {"id": 3},
    ]

    print("Insertion Sort Count: PASS")


def test_binary_search_count():
    records = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
        {"id": 5},
    ]

    result = binary_search_count(
        records,
        3,
        "id"
    )

    assert isinstance(result, dict)
    assert result["index"] == 2
    assert type(result["comparison_count"]) is int
    assert result["comparison_count"] > 0

    missing_result = binary_search_count(
        records,
        99,
        "id"
    )

    assert missing_result["index"] == -1
    assert missing_result["comparison_count"] > 0

    print("Binary Search Count: PASS")


def test_linear_search_count():
    records = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
    ]

    result = linear_search_count(
        records,
        3,
        "id"
    )

    assert isinstance(result, dict)
    assert result["index"] == 2
    assert result["comparison_count"] == 3

    missing_result = linear_search_count(
        records,
        99,
        "id"
    )

    assert missing_result["index"] == -1

    # When absent, linear search should inspect every item
    assert missing_result["comparison_count"] == len(records)

    print("Linear Search Count: PASS")


def main():
    print("\n--- TaskFlow Algorithm Checks ---\n")

    test_insertion_sort()
    test_binary_search()
    test_linear_search()

    test_insertion_sort_count()
    test_binary_search_count()
    test_linear_search_count()

    print("\nALL ALGORITHM TESTS PASSED")


if __name__ == "__main__":
    main()