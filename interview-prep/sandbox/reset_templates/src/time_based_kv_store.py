# P1 - Time-based key/value store
#
# Part 1:
# * set(key, value, timestamp)
# * get(key, timestamp) returns the value at the most recent timestamp <= query.
#
# Part 2:
# * add get_range(key, t_start, t_end).
#
# Part 3:
# * add TTL expiry.
#
# Part 4:
# * add delete operations that interact correctly with historical reads.
class TimeBasedKeyValueStore:
    def __init__(self) -> None:
        raise NotImplementedError

    def set(self, key: str, value: str, timestamp: int) -> None:
        raise NotImplementedError

    def get(self, key: str, timestamp: int) -> str | None:
        raise NotImplementedError

    def get_range(self, key: str, t_start: int, t_end: int) -> list[str]:
        raise NotImplementedError

    def delete(self, key: str, timestamp: int) -> None:
        raise NotImplementedError
