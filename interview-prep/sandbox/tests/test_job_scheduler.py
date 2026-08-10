from job_scheduler import Job, JobScheduler


def test_run_order_respects_dependencies() -> None:
    scheduler = JobScheduler(
        [
            Job("deploy", ["test"]),
            Job("build"),
            Job("test", ["build"]),
        ]
    )

    order = scheduler.run_order()

    assert order.index("build") < order.index("test")
    assert order.index("test") < order.index("deploy")
    assert set(order) == {"build", "test", "deploy"}


def test_independent_jobs_are_included_once() -> None:
    scheduler = JobScheduler([Job("a"), Job("b")])

    assert sorted(scheduler.run_order()) == ["a", "b"]


# Part 2 - cycle detection
#
# def test_cycle_error_names_jobs_in_cycle() -> None:
#     scheduler = JobScheduler([Job("a", ["b"]), Job("b", ["a"])])
#
#     with pytest.raises(CycleError, match="a|b"):
#         scheduler.run_order()
#
#
# Part 3 - bounded parallelism
#
# def test_scheduler_never_runs_more_than_n_workers() -> None:
#     ...
#
#
# Part 4 - retry/backoff/failure propagation
#
# def test_permanently_failed_job_skips_dependents() -> None:
#     ...
#
#
# Part 5 - debugging and hardening
#
# def test_scheduler_never_leaves_job_in_multiple_terminal_states() -> None:
#     ...
#
#
# def test_scheduler_records_retry_count_and_latency_metrics() -> None:
#     ...
