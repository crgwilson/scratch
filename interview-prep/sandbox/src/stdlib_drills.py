"""Small drills for useful operations in Python's standard library."""


def top_k_largest(numbers: list[int], k: int) -> list[int]:
    """Return the ``k`` largest numbers in descending order using ``heapq``.

    Return an empty list when ``k`` is zero. Raise ``ValueError`` when ``k`` is
    negative or larger than the input.
    """
    raise NotImplementedError


def heap_sort(numbers: list[int]) -> list[int]:
    """Heapify a copy of ``numbers``, then drain it into ascending order.

    Do not mutate the caller's list. Practice ``heapify`` and repeated
    ``heappop`` rather than calling ``sorted``.
    """
    raise NotImplementedError


def smallest_and_largest(
    numbers: list[int], k: int
) -> tuple[list[int], list[int]]:
    """Return the ``k`` smallest and ``k`` largest values.

    The smallest list must be ascending and the largest list descending.
    Use the ``heapq`` convenience functions. Assume ``0 <= k <= len(numbers)``.
    """
    raise NotImplementedError


def merge_sorted_lists(lists: list[list[int]]) -> list[int]:
    """Merge any number of already-sorted lists using ``heapq.merge``."""
    raise NotImplementedError


def binary_search(numbers: list[int], target: int) -> int | None:
    """Return the first index of ``target`` in a sorted list, or ``None``.

    Duplicate values make the word "first" important. Use ``bisect`` rather
    than writing the binary-search loop yourself.
    """
    raise NotImplementedError


def values_in_range(numbers: list[int], low: int, high: int) -> list[int]:
    """Return values in the inclusive range [``low``, ``high``].

    ``numbers`` is already sorted. Locate both slice boundaries with bisect.
    Return an empty list when ``low > high``.
    """
    raise NotImplementedError


def insert_sorted(numbers: list[int], value: int) -> list[int]:
    """Insert ``value`` after existing equal values and return the result.

    Keep ``numbers`` sorted, but do not mutate the caller's list. Use an
    ``insort`` operation.
    """
    raise NotImplementedError


def most_common_words(words: list[str], k: int) -> list[tuple[str, int]]:
    """Return the ``k`` most common words and their counts using ``Counter``.

    Ties should retain the order in which a word first appears. Assume ``k``
    is non-negative; requesting more words than exist returns all of them.
    """
    raise NotImplementedError


def inventory_shortfall(
    available: list[str], requested: list[str]
) -> dict[str, int]:
    """Return the positive counts still needed to satisfy a request.

    Treat both lists as multisets. For example, one available ``"bolt"`` and
    three requested ``"bolt"`` values produces ``{"bolt": 2}``. Practice
    ``Counter`` subtraction and return an ordinary dict.
    """
    raise NotImplementedError


def recent_items(items: list[str], capacity: int) -> list[str]:
    """Return the last ``capacity`` items using a bounded ``deque``.

    Preserve their original order. A zero capacity returns an empty list;
    reject a negative capacity with ``ValueError``.
    """
    raise NotImplementedError


def parse_select_query(query: str) -> dict[str, object]:
    """Parse a small SQL ``SELECT`` query using ``re`` capture groups.

    Keywords must be matched case-insensitively and arbitrary whitespace or
    newlines may separate tokens. Support this intentionally limited grammar:

    * one or more comma-separated columns (or ``*``)
    * one table name
    * an optional ``WHERE`` containing simple predicates joined by ``AND``
    * predicate operators ``=``, ``!=``, ``<>``, ``<``, ``<=``, ``>``, ``>=``
    * an optional single-column ``ORDER BY`` with optional ``ASC``/``DESC``
    * an optional integer ``LIMIT`` and optional trailing semicolon

    Identifiers contain letters, numbers, or underscores and cannot start with
    a number. Predicate values are unquoted numbers or single-quoted strings.
    Return this shape, preserving identifier and value spelling from the query::

        {
            "columns": ["name", "age"],
            "table": "users",
            "where": [("active", "=", "1"), ("age", ">=", "21")],
            "order_by": ("name", "ASC"),  # None when absent; ASC by default
            "limit": 10,                  # None when absent
        }

    Strip surrounding quotes from string values. Raise ``ValueError`` when the
    query is outside this grammar. Use named groups for the major clauses and
    capture groups again when parsing each ``WHERE`` predicate.
    """
    raise NotImplementedError
