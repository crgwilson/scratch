from time_based_kv_store import TimeBasedKeyValueStore


def test_get_returns_latest_value_at_or_before_timestamp() -> None:
    store = TimeBasedKeyValueStore()
    store.set("user:1", "draft", 10)
    store.set("user:1", "submitted", 20)
    store.set("user:1", "approved", 30)

    assert store.get("user:1", 5) is None
    assert store.get("user:1", 10) == "draft"
    assert store.get("user:1", 25) == "submitted"
    assert store.get("user:1", 30) == "approved"
    assert store.get("missing", 30) is None


def test_set_can_arrive_out_of_timestamp_order() -> None:
    store = TimeBasedKeyValueStore()
    store.set("k", "newer", 30)
    store.set("k", "older", 10)
    store.set("k", "middle", 20)

    assert store.get("k", 15) == "older"
    assert store.get("k", 25) == "middle"
    assert store.get("k", 35) == "newer"


# Part 2 - get_range
#
# def test_get_range_returns_values_in_timestamp_order() -> None:
#     store = TimeBasedKeyValueStore()
#     store.set("k", "a", 10)
#     store.set("k", "b", 20)
#     store.set("k", "c", 30)
#
#     assert store.get_range("k", 10, 25) == ["a", "b"]
#     assert store.get_range("k", 21, 29) == []
#
#
# Part 3 - TTL expiry
#
# def test_ttl_values_expire_for_future_reads() -> None:
#     store = TimeBasedKeyValueStore(default_ttl=10)
#     store.set("k", "a", 100)
#
#     assert store.get("k", 109) == "a"
#     assert store.get("k", 110) is None
#
#
# Part 4 - historical delete
#
# def test_delete_masks_reads_at_and_after_delete_timestamp() -> None:
#     store = TimeBasedKeyValueStore()
#     store.set("k", "a", 10)
#     store.set("k", "b", 20)
#     store.delete("k", 25)
#
#     assert store.get("k", 24) == "b"
#     assert store.get("k", 25) is None
