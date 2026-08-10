from extended_lru_cache import LRUCache


def test_get_missing_key_returns_none() -> None:
    cache = LRUCache(capacity=2)

    assert cache.get("missing") is None


def test_put_and_get_store_values() -> None:
    cache = LRUCache(capacity=2)

    cache.put("a", "A")
    cache.put("b", "B")

    assert cache.get("a") == "A"
    assert cache.get("b") == "B"


def test_capacity_evicts_least_recently_used_key() -> None:
    cache = LRUCache(capacity=2)
    cache.put("a", "A")
    cache.put("b", "B")
    assert cache.get("a") == "A"

    cache.put("c", "C")

    assert cache.get("a") == "A"
    assert cache.get("b") is None
    assert cache.get("c") == "C"


def test_put_existing_key_updates_value_and_recency() -> None:
    cache = LRUCache(capacity=2)
    cache.put("a", "A")
    cache.put("b", "B")
    cache.put("a", "A2")
    cache.put("c", "C")

    assert cache.get("a") == "A2"
    assert cache.get("b") is None
    assert cache.get("c") == "C"


# Part 2 - per-entry TTL
#
# def test_entry_expires_after_ttl() -> None:
#     cache = LRUCache(capacity=2)
#     cache.put("a", "A", ttl_seconds=10, now=100)
#
#     assert cache.get("a", now=109) == "A"
#     assert cache.get("a", now=110) is None
#
#
# Part 3 - LFU eviction
#
# def test_lfu_evicts_lowest_frequency_then_oldest_tie() -> None:
#     cache = LFUCache(capacity=2)
#     cache.put("a", "A")
#     cache.put("b", "B")
#     cache.get("a")
#     cache.put("c", "C")
#
#     assert cache.get("a") == "A"
#     assert cache.get("b") is None
#
#
# Part 4 - stats
#
# def test_stats_reports_hit_rate() -> None:
#     cache = LRUCache(capacity=2)
#     cache.put("a", "A")
#     cache.get("a")
#     cache.get("missing")
#
#     assert cache.stats()["hits"] == 1
#     assert cache.stats()["misses"] == 1
#     assert cache.stats()["hit_rate"] == 0.5
