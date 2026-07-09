---
tags:
  - coding-exercise
  - interview-prep
  - practical-coding
---
# Multithreaded Web Crawler

## Setup
Given a starting URL, crawl and return every URL reachable from it **within the same domain**. Assume you're given `fetch(url) -> list[str]` that returns the links on a page (it does real network I/O and is slow, ~200ms, and can throw).

For practice, stub it:
```python
import time, random
GRAPH = {
  "a.com/":      ["a.com/1", "a.com/2", "b.com/x"],
  "a.com/1":     ["a.com/2", "a.com/3"],
  "a.com/2":     ["a.com/"],
  "a.com/3":     [],
}
def fetch(url):
    time.sleep(0.2)
    if random.random() < 0.1: raise IOError("timeout")
    return GRAPH.get(url, [])
```

## Part A - Single-threaded
BFS or DFS from the seed; dedupe visited; filter to same domain; return the set. Handle fetch failures (skip? retry once? - state your choice).
## Part B - Multithreaded
Fetches are I/O-bound; parallelize with N worker threads. Requirements:
* No URL fetched twice (visited set must be race-free).
* Program terminates when the frontier is exhausted (the classic hard part - `queue.Queue` + `task_done()`/`join()`, or an in-flight counter).
* No busy-waiting.
## Part C - Politeness / rate limiting
Cap at R requests per second per domain. Simple token bucket or timestamp window shared across workers (locked).

**Verbal follow-ups:**
* Why do threads help here despite the GIL? When would you switch to `asyncio` or multiprocessing?
* Scale it to a distributed crawler: what replaces the in-memory visited set and queue? (This bridges into their system design round — have a 2-minute answer.)
* Retries with backoff; robots.txt; max depth.