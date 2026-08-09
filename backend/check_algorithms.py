from .algorithms import insertion_sort, binary_search, linear_search


def test_insertion_sort():
    tasks = [
        {"title": "High Task", "priority_rank": 3},
        {"title": "Low Task", "priority_rank": 1},
        {"title": "Medium Task", "priority_rank": 2},
    ]

    insertion_sort(tasks, "priority_rank")

    print("Insertion Sort Result:")
    for task in tasks:
        print(task)

    assert tasks[0]["priority_rank"] == 1
    assert tasks[1]["priority_rank"] == 2
    assert tasks[2]["priority_rank"] == 3

    print("Insertion Sort: PASS ✅")
    print()


def test_binary_search():
    tasks = [
        {"id": 1, "title": "Build Task CRUD API"},
        {"id": 2, "title": "Low Priority Task"},
        {"id": 3, "title": "Medium Priority Task"},
    ]

    insertion_sort(tasks, "title")

    result = binary_search(
        tasks,
        "Medium Priority Task",
        "title"
    )

    print("Binary Search Result:")
    print("Index:", result)

    assert result != -1
    assert tasks[result]["title"] == "Medium Priority Task"

    print("Binary Search: PASS ✅")
    print()


def test_linear_search():
    tasks = [
        {"id": 1, "title": "Build Task CRUD API"},
        {"id": 2, "title": "Low Priority Task"},
        {"id": 3, "title": "Medium Priority Task"},
    ]

    result = linear_search(
        tasks,
        "Medium Priority Task",
        "title"
    )

    print("Linear Search Result:")
    print("Index:", result)

    assert result != -1
    assert tasks[result]["title"] == "Medium Priority Task"

    print("Linear Search: PASS ✅")
    print()


def test_not_found():
    tasks = [
        {"id": 1, "title": "Build Task CRUD API"},
        {"id": 2, "title": "Low Priority Task"},
        {"id": 3, "title": "Medium Priority Task"},
    ]

    insertion_sort(tasks, "title")

    result = binary_search(
        tasks,
        "ABCXYZ123",
        "title"
    )

    print("Not Found Test:")
    print("Index:", result)

    assert result == -1

    print("Not Found Test: PASS ✅")
    print()


if __name__ == "__main__":
    print("\n--- TaskFlow Algorithm Tests ---\n")

    test_insertion_sort()
    test_binary_search()
    test_linear_search()
    test_not_found()

    print("ALL ALGORITHM TESTS PASSED ✅")