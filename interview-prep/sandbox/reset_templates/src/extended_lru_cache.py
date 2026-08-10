# P4 - LRU cache, then extended
#
# Part 1:
# * get/put with capacity eviction.
#
# Part 2:
# * add per-entry TTL.
#
# Part 3:
# * change eviction to LFU and discuss the tie-break rule you chose.
#
# Part 4:
# * add stats() for hit rate.
class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity

    def get(self, key: str) -> str | None:
        raise NotImplementedError

    def put(self, key: str, value: str) -> None:
        raise NotImplementedError

    def stats(self) -> dict[str, float | int]:
        raise NotImplementedError
