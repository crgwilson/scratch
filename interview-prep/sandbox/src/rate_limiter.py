# P3 - Rate limiter
#
# Part 1:
# * fixed-window counter per user.
#
# Part 2:
# * convert to sliding window log.
#
# Part 3:
# * convert to token bucket with a refill rate.
# * explain the behavioral difference: fixed windows allow bursts at boundaries,
#   sliding logs smooth exact recent history, token buckets allow saved burst capacity.
#
# Part 4:
# * support multiple limits at once, such as per-second and per-day on the same key.
#
# Part 5:
# * make it distributed with shared state, such as Redis.
# * handle clock skew, reset(key), Redis outage fallback, and replay after recovery.
class FixedWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None:
        raise NotImplementedError

    def allow(self, key: str, timestamp: float) -> bool:
        raise NotImplementedError

    def reset(self, key: str) -> None:
        raise NotImplementedError


class SlidingWindowLogRateLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None:
        raise NotImplementedError

    def allow(self, key: str, timestamp: float) -> bool:
        raise NotImplementedError


class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate_per_second: float) -> None:
        raise NotImplementedError

    def allow(self, key: str, timestamp: float) -> bool:
        raise NotImplementedError


class DistributedRateLimiter:
    def __init__(self, shared_store, local_fallback_store) -> None:
        raise NotImplementedError

    def allow(self, key: str, now_ms: int) -> bool:
        raise NotImplementedError

    def reset(self, key: str) -> None:
        raise NotImplementedError

    def replay_local_events(self) -> None:
        raise NotImplementedError
