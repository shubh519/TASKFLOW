from backend.algorithms import (
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


def create_records(size):
    """
    Create records in reverse order.
    Reverse order is useful for demonstrating
    insertion sort comparison behaviour.
    """
    records = []

    for i in range(size, 0, -1):
        records.append({"id": i})

    return records


def run_benchmark(size):
    print("\n" + "=" * 50)
    print(f"DATASET SIZE: {size}")
    print("=" * 50)

    # Create dataset
    records = create_records(size)

    # -------------------------
    # Insertion Sort
    # -------------------------
    records_for_sort = [record.copy() for record in records]

    sort_comparisons = insertion_sort_count(
        records_for_sort,
        "id"
    )

    print("\nInsertion Sort")
    print("Comparisons:", sort_comparisons)

    # Search for the last ID in the sorted dataset
    target = size

    # -------------------------
    # Linear Search
    # -------------------------
    linear_result = linear_search_count(
        records_for_sort,
        target,
        "id"
    )

    print("\nLinear Search")
    print("Target:", target)
    print("Index:", linear_result["index"])
    print("Comparisons:", linear_result["comparison_count"])

    # -------------------------
    # Binary Search
    # -------------------------
    binary_result = binary_search_count(
        records_for_sort,
        target,
        "id"
    )

    print("\nBinary Search")
    print("Target:", target)
    print("Index:", binary_result["index"])
    print("Comparisons:", binary_result["comparison_count"])


def main():
    dataset_sizes = [10, 100, 500]

    print("TASKFLOW ALGORITHM BENCHMARK")

    for size in dataset_sizes:
        run_benchmark(size)


if __name__ == "__main__":
    main()