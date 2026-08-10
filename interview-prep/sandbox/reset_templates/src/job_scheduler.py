# P7 - Job scheduler with dependencies
#
# Reported variants can be either from-scratch scheduler design or a debugging
# round where you harden existing concurrent scheduler code.
#
# Part 1:
# * run jobs respecting a dependency DAG.
#
# Part 2:
# * detect cycles and report them usefully.
#
# Part 3:
# * add bounded parallelism with N workers.
#
# Part 4:
# * retry with backoff.
# * permanently failed jobs skip dependents rather than hanging.
#
# Part 5:
# * debug a scheduler with pending/running/completed/failed state sets.
# * fix races, deadlocks, incorrect retries, and missing metrics.
class Job:
    def __init__(self, job_id: str, dependencies: list[str] | None = None) -> None:
        raise NotImplementedError


class JobScheduler:
    def __init__(self, jobs: list[Job]) -> None:
        raise NotImplementedError

    def run_order(self) -> list[str]:
        raise NotImplementedError


class CycleError(Exception):
    pass
