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
class FixedWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit = limit
        self.window_seconds = window_seconds

    def allow(self, key: str, timestamp: float) -> bool:
        raise NotImplementedError


class SlidingWindowLogRateLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit = limit
        self.window_seconds = window_seconds

    def allow(self, key: str, timestamp: float) -> bool:
        raise NotImplementedError


class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate_per_second: float) -> None:
        self.capacity = capacity
        self.refill_rate_per_second = refill_rate_per_second

    def allow(self, key: str, timestamp: float) -> bool:
        raise NotImplementedError
