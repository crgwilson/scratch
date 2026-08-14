# Practice Problem Answers

This guide is meant as a study aid, not as the first thing to read before doing a rep. Use it when you get stuck, then reset the source and try again from memory.

## P1 - Time-based Key/Value Store

### Part 1 - set and get at timestamp

Store each key as a sorted list of `(timestamp, value)` pairs. `set` appends if timestamps arrive in increasing order, otherwise insert while preserving sort order. `get` uses binary search to find the rightmost timestamp less than or equal to the query timestamp.

Tradeoffs:
- A list plus binary search gives `O(log n)` reads and `O(1)` appends for ordered writes.
- Out-of-order writes cost `O(n)` because insertion shifts list elements.
- A balanced tree would improve arbitrary inserts, but is usually overkill in Python interviews unless the prompt stresses out-of-order writes.

```python
from bisect import bisect_right


class TimeBasedKeyValueStore:
    def __init__(self):
        self.store = {}

    def set(self, key, value, timestamp):
        entries = self.store.setdefault(key, [])
        if not entries or entries[-1][0] <= timestamp:
            entries.append((timestamp, value))
            return

        index = bisect_right([ts for ts, _ in entries], timestamp)
        entries.insert(index, (timestamp, value))

    def get(self, key, timestamp):
        entries = self.store.get(key, [])
        timestamps = [ts for ts, _ in entries]
        index = bisect_right(timestamps, timestamp) - 1
        if index < 0:
            return None
        return entries[index][1]
```

### Part 2 - get_range

Use two binary searches: left boundary at `t_start`, right boundary after `t_end`.

```python
def get_range(self, key, t_start, t_end):
    entries = self.store.get(key, [])
    timestamps = [ts for ts, _ in entries]
    left = bisect_left(timestamps, t_start)
    right = bisect_right(timestamps, t_end)
    return [value for _, value in entries[left:right]]
```

### Part 3 - TTL expiry

Store expiry metadata with each value, such as `(timestamp, value, expires_at)`. A read finds the latest candidate at or before the query timestamp, then checks whether `timestamp < expires_at`.

Tradeoff: if the latest value is expired, decide whether to return an older unexpired value or `None`. Most systems treat a newer expired write as no longer visible and do not fall back to older values. State this assumption.

```python
def set(self, key, value, timestamp, ttl=None):
    expires_at = None if ttl is None else timestamp + ttl
    self.store.setdefault(key, []).append((timestamp, value, expires_at))

def get(self, key, timestamp):
    entry = self._latest_entry_at_or_before(key, timestamp)
    if entry is None:
        return None
    _, value, expires_at = entry
    if expires_at is not None and timestamp >= expires_at:
        return None
    return value
```

### Part 4 - delete and historical reads

Represent deletes as tombstones in the same timeline. This makes delete history explicit and keeps binary search logic simple.

```python
def delete(self, key, timestamp):
    self.store.setdefault(key, []).append((timestamp, None, None, True))

def get(self, key, timestamp):
    entry = self._latest_entry_at_or_before(key, timestamp)
    if entry is None:
        return None
    _, value, expires_at, deleted = entry
    if deleted:
        return None
    if expires_at is not None and timestamp >= expires_at:
        return None
    return value
```

Historical reads before the delete still see old values. Reads at or after the delete return `None` until another `set` happens.

## P2 - Resumable Iterator

### Part A - generic contract test

Capture state before every call to `next()`, including the call that discovers
exhaustion. Each state must work on a fresh iterator, so the test does not rely
on the state's representation.

```python
import pytest

def test_iterator(make_iter, expected_elements):
    iterator = make_iter()
    states = []
    actual = []

    while True:
        states.append(iterator.checkpoint())
        try:
            actual.append(next(iterator))
        except StopIteration:
            break

    assert actual == list(expected_elements)
    assert iter(iterator) is iterator
    with pytest.raises(StopIteration):
        next(iterator)

    for consumed, state in enumerate(states):
        resumed = make_iter()
        resumed.resume(state)
        assert list(resumed) == list(expected_elements[consumed:])
        with pytest.raises(StopIteration):
            next(resumed)
```

In a pytest file, set `test_iterator.__test__ = False` if it is invoked as a
helper; otherwise pytest will interpret its arguments as fixture names.

### Part B - list iterator

The next list position is an implementation detail. Although this implementation
uses an integer, callers only store and return the opaque value.

```python
class ResumableListIterator(ResumableIterator):
    def __init__(self, items: list):
        self._items = items
        self._index = 0

    def __next__(self):
        if self._index >= len(self._items):
            raise StopIteration
        item = self._items[self._index]
        self._index += 1
        return item

    def checkpoint(self):
        return self._index

    def resume(self, state):
        self._index = state
```

An interview-ready implementation may validate that `state` is an integer in
`[0, len(items)]`, but validation is not essential to the core algorithm.

### Part C - multi-file iterator by composition

The outer state is a pair: the current file index and that file iterator's
opaque state. Do not inspect or reinterpret the inner state. The sentinel state
`(len(paths), None)` represents complete exhaustion.

```python
class ResumableMultiFileIterator(ResumableIterator):
    def __init__(self, paths: list[str]):
        self._paths = paths
        self._file_index = 0
        self._current = (
            ResumableFileIterator(paths[0]) if paths else None
        )

    def __next__(self):
        while self._current is not None:
            try:
                return next(self._current)
            except StopIteration:
                self._file_index += 1
                if self._file_index == len(self._paths):
                    self._current = None
                else:
                    self._current = ResumableFileIterator(
                        self._paths[self._file_index]
                    )
        raise StopIteration

    def checkpoint(self):
        if self._current is None:
            return (len(self._paths), None)
        return (self._file_index, self._current.checkpoint())

    def resume(self, state):
        file_index, inner_state = state
        self._file_index = file_index

        if file_index == len(self._paths):
            self._current = None
            return

        self._current = ResumableFileIterator(self._paths[file_index])
        self._current.resume(inner_state)
```

The `while` loop is what handles any number of consecutive empty files. For
local tests, replace `ResumableFileIterator` with `ResumableListIterator` and
pass a list of per-file lists.

### Part D - async version

Use `__aiter__` and `async def __anext__`, awaiting the inner iterator's
`__anext__()`. State capture must be serialized with reads - typically with an
`asyncio.Lock` - so `checkpoint()` cannot observe a read after it starts but before
the position commits. Another defensible contract forbids state capture while
`__anext__()` is in flight.

### Verbal follow-ups

- If a file changes, byte offsets or record indexes may resume at the wrong
  logical record. Store file identity/version metadata, require immutable files,
  or use stable record IDs.
- For persistence, encode the outer state plus the inner iterator's serializable
  state as versioned JSON. Include enough source identity to reject incompatible
  restores.
- A resumable 2D iterator is the same composition: store the outer-list index
  plus the inner-list iterator state, and skip empty inner lists with a loop.

## P3 - Rate Limiter

### Part 1 - fixed-window counter per user

Bucket requests by `timestamp // window_seconds`. Store a `(window_id, count)` per key.

```python
class FixedWindowRateLimiter:
    def __init__(self, limit, window_seconds):
        self.limit = limit
        self.window_seconds = window_seconds
        self.counts = {}

    def allow(self, key, timestamp):
        window = int(timestamp // self.window_seconds)
        current_window, count = self.counts.get(key, (window, 0))
        if current_window != window:
            current_window, count = window, 0
        if count >= self.limit:
            self.counts[key] = (current_window, count)
            return False
        self.counts[key] = (current_window, count + 1)
        return True

    def reset(self, key):
        self.counts.pop(key, None)
```

Tradeoff: simple and memory efficient, but allows boundary bursts. A user can send `limit` requests at the end of one window and `limit` more at the start of the next.

### Part 2 - sliding window log

Store recent request timestamps per key. Drop timestamps outside the window, then allow only if the remaining count is below the limit.

```python
from collections import defaultdict, deque

class SlidingWindowLogRateLimiter:
    def __init__(self, limit, window_seconds):
        self.limit = limit
        self.window_seconds = window_seconds
        self.logs = defaultdict(deque)

    def allow(self, key, timestamp):
        log = self.logs[key]
        cutoff = timestamp - self.window_seconds
        while log and log[0] <= cutoff:
            log.popleft()
        if len(log) >= self.limit:
            return False
        log.append(timestamp)
        return True
```

Tradeoff: precise but memory grows with request volume.

### Part 3 - token bucket

Each key has tokens and last refill time. Refill based on elapsed time, capped by capacity.

```python
class TokenBucketRateLimiter:
    def __init__(self, capacity, refill_rate_per_second):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_second
        self.buckets = {}

    def allow(self, key, timestamp):
        tokens, last_seen = self.buckets.get(key, (self.capacity, timestamp))
        tokens = min(self.capacity, tokens + (timestamp - last_seen) * self.refill_rate)
        if tokens < 1:
            self.buckets[key] = (tokens, timestamp)
            return False
        self.buckets[key] = (tokens - 1, timestamp)
        return True
```

Behavior difference:
- Fixed window is cheapest but bursty at boundaries.
- Sliding log is precise over the last N seconds.
- Token bucket smooths average rate while allowing stored burst capacity.

### Part 4 - multiple limits

Compose limiters. A request is allowed only if all limits allow. For production correctness, check all limits before mutating any counters, or support rollback.

```python
class CompositeLimiter:
    def __init__(self, limiters):
        self.limiters = limiters

    def allow(self, key, timestamp):
        return all(limiter.allow(key, timestamp) for limiter in self.limiters)
```

In an interview, mention the mutation issue. The simple code may consume one limiter before another rejects.

### Part 5 - distributed limiter, reset, fallback, and replay

Reported OpenAI variants often push rate limiting into distributed state. The normal answer is Redis because it gives shared state across stateless application servers and atomic operations.

For a sliding-window log, Redis sorted sets are a clean fit:
- key: rate-limit key, such as user ID or API key
- score: request timestamp in milliseconds
- member: unique request ID
- operation: remove old scores, count current scores, add current request if below limit, set TTL

Use a Lua script or Redis transaction so count and add are atomic.

```python
def allow_distributed(redis, key, now_ms, limit, window_ms, request_id):
    redis.zremrangebyscore(key, 0, now_ms - window_ms)
    count = redis.zcard(key)
    if count >= limit:
        return False
    redis.zadd(key, {request_id: now_ms})
    redis.expire(key, int(window_ms / 1000) + 1)
    return True
```

Clock skew: prefer server-side Redis time or a single trusted time source. If each app server passes its own clock, skew can incorrectly allow or reject requests.

`reset(key)` should delete the limiter state for that key.

Redis outage fallback: decide fail-open vs fail-closed. A practical degraded mode is local in-process or local-file limiting with an async replay queue. This is approximate because each server only sees local traffic during the outage.

Tradeoffs:
- fail-open protects availability but can exceed quota
- fail-closed protects quota but can cause user-visible outages
- local fallback is best-effort and needs observability so operators know accuracy is degraded

## P4 - LRU Cache, Then Extended

### Part 1 - get/put with capacity eviction

Use a dict for key to node lookup and a doubly linked list for recency. Head is least recent, tail is most recent. Sentinel nodes simplify edge cases.

```python
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.lookup = {}
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        node = self.lookup.get(key)
        if node is None:
            return None
        self._move_to_tail(node)
        return node.value

    def put(self, key, value):
        if key in self.lookup:
            node = self.lookup[key]
            node.value = value
            self._move_to_tail(node)
            return
        if len(self.lookup) == self.capacity:
            self._evict_head()
        node = Node(key, value)
        self.lookup[key] = node
        self._append(node)
```

### Part 2 - per-entry TTL

Add `expires_at` to the node. On `get`, treat expired entries as missing and remove them. On `put`, store the expiration.

Tradeoff: lazy cleanup is simple. Eager cleanup requires a min-heap or background process keyed by expiry.

### Part 3 - LFU eviction

Use frequency buckets. Map key to node, and map frequency to an ordered dict of keys. Track `min_freq` for eviction.

Tie-break rule: evict the least recently used key among the lowest-frequency keys. This is easy to explain and common.

```python
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.values = {}
        self.freq = {}
        self.buckets = defaultdict(OrderedDict)
        self.min_freq = 0
```

On access, remove the key from its old frequency bucket, increment its frequency, and append it to the new bucket.

### Part 4 - stats

Track `hits` and `misses` in `get`.

```python
def stats(self):
    total = self.hits + self.misses
    return {
        "hits": self.hits,
        "misses": self.misses,
        "hit_rate": 0 if total == 0 else self.hits / total,
    }
```

Decide whether expired entries count as misses. Usually they should.

## P5 - Mini SQL / Expression Evaluator

### Part 1 - SELECT columns FROM table WHERE col = value

Keep structure separate:
- Tokenizer turns a string into tokens.
- Parser turns tokens into an AST or query object.
- Executor applies the parsed query to tables.

```python
from dataclasses import dataclass

@dataclass
class Query:
    columns: list[str]
    table: str
    where_column: str
    where_value: object
```

Execution is filtering then projection.

```python
def execute(query, tables):
    parsed = Parser().parse(query)
    rows = tables[parsed.table]
    filtered = [row for row in rows if row.get(parsed.where_column) == parsed.where_value]
    return [{col: row.get(col) for col in parsed.columns} for row in filtered]
```

Tradeoff: do not try to support SQL generally. Define the grammar you support and reject everything else.

### Part 2 - AND/OR

Represent WHERE as an expression tree.

```python
@dataclass
class Eq:
    column: str
    value: object

@dataclass
class And:
    left: object
    right: object

@dataclass
class Or:
    left: object
    right: object

def eval_expr(expr, row):
    if isinstance(expr, Eq):
        return row.get(expr.column) == expr.value
    if isinstance(expr, And):
        return eval_expr(expr.left, row) and eval_expr(expr.right, row)
    if isinstance(expr, Or):
        return eval_expr(expr.left, row) or eval_expr(expr.right, row)
```

Mention precedence. Usually `AND` binds tighter than `OR`.

### Part 3 - ORDER BY and LIMIT

Apply order after filtering and before limit. Projection can happen before or after ordering only if the ORDER BY column is still available.

```python
rows = [row for row in rows if eval_expr(parsed.where, row)]
if parsed.order_by:
    rows.sort(key=lambda row: row.get(parsed.order_by))
if parsed.limit is not None:
    rows = rows[:parsed.limit]
return [project(row, parsed.columns) for row in rows]
```

### Part 4 - aggregates and GROUP BY

Group rows by the group-by column, then compute aggregate functions per group.

```python
from collections import defaultdict

groups = defaultdict(list)
for row in rows:
    groups[row[group_by]].append(row)

result = []
for key, group_rows in groups.items():
    result.append({
        group_by: key,
        "count": len(group_rows),
        "sum_total": sum(row["total"] for row in group_rows),
    })
```

Tradeoff: hardcoding aggregate output names is fine for a drill, but a cleaner parser should preserve aliases or derive names consistently.

### Part 5 - INNER JOIN

For a two-table inner join, parse table names, aliases if supported, and the equality join condition. The executor can use a nested loop first, then optimize with a hash join.

Nested loop is simplest:

```python
joined = []
for left in users:
    for right in orders:
        if left["id"] == right["user_id"]:
            joined.append({"users": left, "orders": right})
```

Hash join is better when one side can be indexed:

```python
index = {}
for order in orders:
    index.setdefault(order["user_id"], []).append(order)

joined = []
for user in users:
    for order in index.get(user["id"], []):
        joined.append((user, order))
```

Tradeoff: prefix columns internally, such as `users.name`, so duplicate column names do not collide.

### Part 6 - window functions

A simple `ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY total)` can be implemented by grouping rows by partition key, sorting each group, then assigning numbers.

```python
groups = defaultdict(list)
for row in rows:
    groups[row[partition_by]].append(row)

output = []
for _, group in groups.items():
    group.sort(key=lambda row: row[order_by])
    for index, row in enumerate(group, start=1):
        new_row = dict(row)
        new_row["row_number"] = index
        output.append(new_row)
```

Keep this deliberately narrow. A full SQL window engine is much larger than the interview prompt usually needs.

## P6 - Sync Local State to Cloud / Persistent Key-Value Store

### Part 1 - upload all keys

Convert strings to bytes and call remote `put` for each key.

```python
def sync(local, remote):
    for key, value in local.items():
        remote.put(key, string_to_bytes(value))
```

### Part 2 - only changed keys

Keep a local manifest of key to checksum or version. Upload only when the checksum differs from the last synced checksum.

```python
import hashlib

def checksum(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
```

Tradeoff: comparing content costs CPU but avoids unnecessary network writes. Comparing modified timestamps is cheaper but less reliable.

### Part 3 - partial upload failure

Update the manifest only after a key uploads successfully. Return or raise a useful error containing failed keys. Retrying should be safe because already uploaded unchanged keys can be skipped.

```python
def sync(local, remote, manifest):
    failed = []
    for key, value in local.items():
        digest = checksum(value)
        if manifest.get(key) == digest:
            continue
        try:
            remote.put(key, string_to_bytes(value))
            manifest[key] = digest
        except Exception:
            failed.append(key)
    if failed:
        raise SyncError(failed)
```

### Part 4 - two clients writing concurrently

Use optimistic concurrency. Remote `put` should take an expected version or etag. If the etag changed, fail with conflict and force caller to merge or retry.

```python
remote.put(key, value_bytes, expected_version=known_version)
```

Explain conflict policy: last-write-wins is simple but can lose data. Compare-and-swap with explicit conflict handling is safer.

### Part 5 - append-only persistence

Reported variants often ask for a persistent key-value store rather than cloud sync specifically. The clean interview design is an in-memory dict plus append-only log.

Each mutation writes a record:

```text
PUT key value
DEL key
```

On startup, replay the log from the beginning to rebuild the dict.

```python
def put(self, key, value):
    self.data[key] = value
    self.log.write(encode_record("PUT", key, value))
    self.log.flush()

def delete(self, key):
    self.data.pop(key, None)
    self.log.write(encode_record("DEL", key))
    self.log.flush()
```

Tradeoffs:
- append-only logs make writes simple and recovery straightforward
- the file grows forever unless you add snapshots or compaction
- flushing every write is safer but slower

### Part 6 - partial write recovery

Use length-prefixed records or checksums. During recovery, stop at the first incomplete or corrupt trailing record.

```python
def recover(path):
    data = {}
    for record in read_valid_records_until_corruption(path):
        apply_record(data, record)
    return data
```

This handles process crashes during a write. In a real system, write to a temp file and atomic rename for snapshots.

## P7 - Job Scheduler With Dependencies

Reported variants can be from-scratch DAG scheduling or debugging existing concurrent scheduler code. Treat both as testing the same core ideas: state transitions, dependency invariants, retries, and no hanging dependents.

### Part 1 - run jobs respecting a DAG

Topological sort. Build adjacency list and indegree counts. Start with jobs that have zero indegree.

```python
from collections import defaultdict, deque

def run_order(jobs):
    graph = defaultdict(list)
    indegree = {job.job_id: 0 for job in jobs}
    for job in jobs:
        for dep in job.dependencies:
            graph[dep].append(job.job_id)
            indegree[job.job_id] += 1

    ready = deque([job_id for job_id, count in indegree.items() if count == 0])
    order = []
    while ready:
        job_id = ready.popleft()
        order.append(job_id)
        for child in graph[job_id]:
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
    return order
```

### Part 2 - detect cycles usefully

After topological sort, if output count is smaller than job count, nodes with positive indegree are in or blocked by a cycle. Report those IDs.

```python
remaining = [job_id for job_id, count in indegree.items() if count > 0]
if remaining:
    raise CycleError(f"cycle involving: {remaining}")
```

### Part 3 - bounded parallelism

Use a queue of ready jobs and at most N workers. When a job completes, decrement indegrees for dependents and enqueue newly ready jobs.

Tradeoff: threads are fine for I/O-bound jobs. CPU-bound jobs need processes or an async/external worker system.

### Part 4 - retry, backoff, and dependent skip

Track job states: pending, running, succeeded, failed, skipped. A failed job after max retries causes all dependents that require it to be skipped.

```python
for attempt in range(max_attempts):
    try:
        run_job(job)
        mark_succeeded(job)
        break
    except Exception:
        sleep(backoff(attempt))
else:
    mark_failed(job)
    skip_dependents(job)
```

Important interviewer point: dependents must not hang waiting for a dependency that will never succeed.

### Part 5 - debugging and hardening an existing scheduler

If handed existing code, start by identifying invariants:
- a job is in exactly one state set
- a terminal job never moves back to running
- retry count increments once per failed attempt
- no more than N jobs run at once
- no more than R jobs start per second if a start-rate limit exists
- dependents of permanent failures are skipped or marked blocked

Useful fixes:
- protect multi-step state transitions with a lock
- use a queue for ready jobs
- separate worker concurrency from start-rate limiting
- record start time, finish time, latency, retry count, and final status
- make job execution idempotent or document at-least-once semantics

Tests should reproduce the original bug. For example, if a race puts a job in both `completed` and `failed`, write a test that forces two workers through that path before refactoring.

## P8 - IP Address Iterator

### Part 1 - iterate a CIDR block

Use the standard `ipaddress` module. It handles parsing and integer conversion correctly.

```python
import ipaddress

class CIDRIterator:
    def __init__(self, cidr):
        self.network = ipaddress.ip_network(cidr, strict=False)

    def __iter__(self):
        for address in self.network:
            yield str(address)
```

Tradeoff: `network.hosts()` skips network and broadcast addresses for IPv4. The prompt says every address, so iterate over `network` directly.

### Part 2 - multiple overlapping blocks without duplicates

Keep a set of emitted integer addresses. This is fine for small inputs but not memory-flat.

```python
class MultiCIDRIterator:
    def __iter__(self):
        seen = set()
        for cidr in self.cidrs:
            for address in ipaddress.ip_network(cidr, strict=False):
                value = int(address)
                if value in seen:
                    continue
                seen.add(value)
                yield str(address)
```

### Part 3 - lazy and memory-flat for /8

Normalize CIDR blocks into integer intervals, sort and merge intervals, then lazily count from start to end. This avoids storing every IP.

```python
def cidr_to_interval(cidr):
    network = ipaddress.ip_network(cidr, strict=False)
    return int(network.network_address), int(network.broadcast_address)

def merge_intervals(intervals):
    intervals.sort()
    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1] + 1:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged
```

Then yield each integer as an IP address:

```python
for start, end in merged:
    for value in range(start, end + 1):
        yield str(ipaddress.ip_address(value))
```

## P9 - Refactoring Drill

### Part 1 - characterize existing behavior

Before refactoring, add tests that lock down current behavior. The active tests do this for `order_report`.

What to preserve:
- cancelled rows are excluded
- missing totals count as 0
- missing customers are grouped as `"unknown"`
- output shape stays `{"count", "total", "by_customer"}`

### Part 2 - improve names and extract helpers

Replace vague names with domain names. Extract small helpers only when they clarify intent.

```python
def is_counted_order(order):
    return order.get("status") != "cancelled"

def order_total(order):
    return order.get("total", 0)

def customer_name(order):
    return order.get("customer", "unknown")
```

### Part 3 - fix the latent bug

The likely bug is that non-numeric or `None` totals can break summing. Decide whether to reject invalid rows or coerce missing/None totals to 0.

```python
def order_total(order):
    total = order.get("total", 0)
    return 0 if total is None else total
```

State the policy clearly.

### Part 4 - narrate tradeoffs

Useful narration:
- "I am first preserving behavior with characterization tests."
- "Now I am renaming variables before changing logic so the code tells me what it does."
- "I am extracting total/customer helpers because defaults are business rules."
- "I am keeping the return shape stable because callers may rely on it."

This drill is less about clever algorithms and more about showing controlled, low-risk improvement.
