# P7 - Job scheduler with dependencies
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
class Job:
    def __init__(self, job_id: str, dependencies: list[str] | None = None) -> None:
        self.job_id = job_id
        self.dependencies = dependencies or []


class JobScheduler:
    def __init__(self, jobs: list[Job]) -> None:
        self.jobs = jobs

    def run_order(self) -> list[str]:
        raise NotImplementedError


class CycleError(Exception):
    pass
