from rate_limiter import FixedWindowRateLimiter


def test_fixed_window_allows_up_to_limit_per_key() -> None:
    limiter = FixedWindowRateLimiter(limit=2, window_seconds=60)

    assert limiter.allow("alice", 0) is True
    assert limiter.allow("alice", 1) is True
    assert limiter.allow("alice", 2) is False
    assert limiter.allow("bob", 2) is True


def test_fixed_window_resets_at_window_boundary() -> None:
    limiter = FixedWindowRateLimiter(limit=2, window_seconds=60)

    assert limiter.allow("alice", 58) is True
    assert limiter.allow("alice", 59) is True
    assert limiter.allow("alice", 60) is True
    assert limiter.allow("alice", 61) is True
    assert limiter.allow("alice", 62) is False


# Part 2 - sliding window log
#
# def test_sliding_window_log_counts_only_recent_requests() -> None:
#     limiter = SlidingWindowLogRateLimiter(limit=2, window_seconds=60)
#
#     assert limiter.allow("alice", 0) is True
#     assert limiter.allow("alice", 59) is True
#     assert limiter.allow("alice", 60) is False
#     assert limiter.allow("alice", 61) is True
#
#
# Part 3 - token bucket
#
# def test_token_bucket_refills_over_time() -> None:
#     limiter = TokenBucketRateLimiter(capacity=2, refill_rate_per_second=1)
#
#     assert limiter.allow("alice", 0) is True
#     assert limiter.allow("alice", 0) is True
#     assert limiter.allow("alice", 0) is False
#     assert limiter.allow("alice", 1) is True
#
#
# Part 4 - multiple limits
#
# def test_composite_limiter_requires_all_limits_to_allow() -> None:
#     ...
