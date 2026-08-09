from backend.algorithms import (
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


def main():
    # Sample task data
    records = [
        {"id": 5},
        {"id": 2},
        {"id": 8},
        {"id": 1},
        {"id": 9},
        {"id": 3},
        {"id": 7},
        {"id": 4},
        {"id": 6},
    ]

    # -----------------------------
    # Insertion Sort Benchmark
    # -----------------------------
    records_for_sort = [record.copy() for record in records]

    sort_comparisons = insertion_sort_count(
        records_for_sort,
        "id"
    )

    print("Insertion Sort")
    print("Sorted records:", records_for_sort)
    print("Comparisons:", sort_comparisons)

    # -----------------------------
    # Linear Search Benchmark
    # -----------------------------
    target = 7

    linear_result = linear_search_count(
        records_for_sort,
        target,
        "id"
    )

    print("\nLinear Search")
    print("Target:", target)
    print("Index:", linear_result["index"])
    print("Comparisons:", linear_result["comparison_count"])

    # -----------------------------
    # Binary Search Benchmark
    # -----------------------------
    binary_result = binary_search_count(
        records_for_sort,
        target,
        "id"
    )

    print("\nBinary Search")
    print("Target:", target)
    print("Index:", binary_result["index"])
    print("Comparisons:", binary_result["comparison_count"])


if __name__ == "__main__":
    main()