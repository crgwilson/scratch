import pytest

from stdlib_drills import (
    binary_search,
    heap_sort,
    insert_sorted,
    inventory_shortfall,
    merge_sorted_lists,
    most_common_words,
    parse_select_query,
    recent_items,
    smallest_and_largest,
    top_k_largest,
    values_in_range,
)


def test_top_k_largest() -> None:
    assert top_k_largest([8, 1, 5, 2, 9, 9, 3], 3) == [9, 9, 8]
    assert top_k_largest([3, 1], 0) == []


@pytest.mark.parametrize("k", [-1, 4])
def test_top_k_largest_rejects_invalid_k(k: int) -> None:
    with pytest.raises(ValueError):
        top_k_largest([1, 2, 3], k)


def test_heap_sort_does_not_mutate_input() -> None:
    numbers = [5, -1, 5, 2, 0]
    assert heap_sort(numbers) == [-1, 0, 2, 5, 5]
    assert numbers == [5, -1, 5, 2, 0]


def test_smallest_and_largest() -> None:
    numbers = [7, 2, 9, 2, 4, 11]
    assert smallest_and_largest(numbers, 3) == ([2, 2, 4], [11, 9, 7])
    assert smallest_and_largest(numbers, 0) == ([], [])


def test_merge_sorted_lists() -> None:
    assert merge_sorted_lists([[1, 4, 8], [], [2, 2, 9], [-3, 10]]) == [
        -3,
        1,
        2,
        2,
        4,
        8,
        9,
        10,
    ]
    assert merge_sorted_lists([]) == []


def test_binary_search_returns_first_match() -> None:
    numbers = [1, 4, 4, 4, 9]
    assert binary_search(numbers, 4) == 1
    assert binary_search(numbers, 6) is None
    assert binary_search([], 1) is None


def test_values_in_inclusive_range() -> None:
    numbers = [1, 2, 2, 4, 5, 7, 7, 9]
    assert values_in_range(numbers, 2, 7) == [2, 2, 4, 5, 7, 7]
    assert values_in_range(numbers, 3, 6) == [4, 5]
    assert values_in_range(numbers, 8, 3) == []


def test_insert_sorted_does_not_mutate_input() -> None:
    numbers = [1, 3, 3, 8]
    assert insert_sorted(numbers, 3) == [1, 3, 3, 3, 8]
    assert numbers == [1, 3, 3, 8]


def test_most_common_words_preserves_first_seen_ties() -> None:
    words = ["pear", "apple", "pear", "plum", "apple", "pear", "plum"]
    assert most_common_words(words, 2) == [("pear", 3), ("apple", 2)]
    assert most_common_words(["b", "a", "a", "b"], 2) == [
        ("b", 2),
        ("a", 2),
    ]
    assert most_common_words(words, 0) == []


def test_inventory_shortfall() -> None:
    available = ["bolt", "nut", "bolt", "washer"]
    requested = ["bolt", "bolt", "bolt", "nut", "screw", "screw"]
    assert inventory_shortfall(available, requested) == {"bolt": 1, "screw": 2}


def test_recent_items() -> None:
    assert recent_items(["a", "b", "c", "d"], 3) == ["b", "c", "d"]
    assert recent_items(["a", "b"], 5) == ["a", "b"]
    assert recent_items(["a"], 0) == []


def test_recent_items_rejects_negative_capacity() -> None:
    with pytest.raises(ValueError):
        recent_items(["a"], -1)


def test_parse_select_query_with_all_clauses() -> None:
    query = """
        select name, email, login_count
        from Users
        where active = 1 AND plan = 'pro' and login_count >= 10
        order by login_count desc
        limit 25;
    """
    assert parse_select_query(query) == {
        "columns": ["name", "email", "login_count"],
        "table": "Users",
        "where": [
            ("active", "=", "1"),
            ("plan", "=", "pro"),
            ("login_count", ">=", "10"),
        ],
        "order_by": ("login_count", "DESC"),
        "limit": 25,
    }


def test_parse_select_query_handles_optional_clauses() -> None:
    assert parse_select_query("SELECT * FROM audit_log") == {
        "columns": ["*"],
        "table": "audit_log",
        "where": [],
        "order_by": None,
        "limit": None,
    }
    assert parse_select_query("SeLeCt id FROM jobs OrDeR By created_at") == {
        "columns": ["id"],
        "table": "jobs",
        "where": [],
        "order_by": ("created_at", "ASC"),
        "limit": None,
    }


def test_parse_select_query_supports_operators_and_negative_numbers() -> None:
    query = "SELECT id FROM readings WHERE temperature < -2.5 AND status != 'bad'"
    assert parse_select_query(query)["where"] == [
        ("temperature", "<", "-2.5"),
        ("status", "!=", "bad"),
    ]


@pytest.mark.parametrize(
    "query",
    [
        "SELECT id users",
        "SELECT id FROM users WHERE active IN (1, 2)",
        "SELECT id FROM users LIMIT many",
    ],
)
def test_parse_select_query_rejects_unsupported_sql(query: str) -> None:
    with pytest.raises(ValueError):
        parse_select_query(query)
