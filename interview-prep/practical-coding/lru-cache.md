---
tags:
  - coding-exercise
  - interview-prep
  - practical-coding
---
# LRU Cache (warm-up classic, most-reported single question)
## Part A:
```python
c = LRUCache(capacity=2)
c.put(1, "a"); c.put(2, "b")
c.get(1)        # "a"  (1 is now most recent)
c.put(3, "c")   # evicts 2
c.get(2)        # -1 / None
```
Do it twice in practice: once with `OrderedDict.move_to_end`/`popitem(last=False)`, once hand-rolled with hashmap + doubly linked list with sentinel head/tail. Both O(1).

Important tips for this part -
1. You need both a doubly linked list, and a dict here. The dict mapping key to linked list node allowing for O(1) retrieval, and a doubly linked list to more easily detach nodes
2. Aside from the obvious, get and put methods, you'll want a detach, to pull out nodes, a pop, to pop off the head (reuse detach here), and a move_to_back (again, reuse detech)
3. Use dummy sentinel values for the head and tail, that will make it way easier to move things around without a bunch of null checks.
## Part B - TTL
Entries expire N seconds after insert. Lazy expiry on access vs. background sweeper - implement lazy, discuss sweeper.
## Part C - Thread safety
Wrap operations in a lock; discuss why `get` also mutates (recency update) so even reads need the write lock; mention lock-free/sharded designs as the scale answer.








# LRU Cache — 4-Part Interview Guide

Reference for a 60-minute CoderPad round. Parts escalate; reaching partway through Part 3 is a good outcome, not a shortfall.

---

## Two patterns that carry the whole problem

**1. Purge-then-act.** Once TTL exists, every public method starts by purging expired entries, then does its job. One principle instead of four patches.

**2. The heap suggests, the dict decides.** A heap can't locate elements in its middle, so never update it in place — push an immutable snapshot and validate the root against the live node before trusting it. Applies to both heaps (priority and expiry).

---

## Part 1 — Base LRU

### Clarifying questions

- Can I use `OrderedDict`? (Frame it as knowledge, not a request — see script below.)
- Does `put` on an existing key count as a use? → **Yes**, bumps recency.
- Return `-1` or `None` on a miss? → Either; be consistent and say which.
- Is capacity guaranteed positive? → Determines `==` vs `>=` on the capacity check, and whether capacity 0 is a real case.

### Opening script (rehearse this out loud)

> "`OrderedDict` implements exactly this — a dict over a doubly-linked list. I'm assuming you want the mechanics, so I'll build it by hand, but flagging I'd reach for the stdlib in real code.
> 
> Two structures. A **doubly-linked list** tracks recency: on access I move the node to the MRU end, so eviction is just removing from the LRU end — O(1), no scanning or tallying. It has to be doubly-linked because when I move a node from the middle, a singly-linked list gives me no way to reach its predecessor without an O(n) scan.
> 
> That handles recency but not lookup, so I also keep a **dict mapping key → node**, and the node holds the value. The node also stores **its own key**, specifically so eviction can reverse-map into the dict.
> 
> Neither structure alone works. A plain dict preserves _insertion_ order in modern Python but gives no way to reorder — no `move_to_end` equivalent — and finding the LRU key means scanning. A plain list gives ordering but O(n) to find a key, and O(n) again to remove from the middle since every subsequent element shifts down an index.
> 
> For edge cases I'll use **two sentinel nodes** — a permanent dummy head and tail that sit outside the data. Every real node then always has both neighbours, so unlink is unconditional with no null checks. `self.head.next` is the LRU end, `self.tail.prev` is the MRU end, and the cache is empty exactly when `self.head.next is self.tail`.
> 
> Both operations are O(1); space is O(capacity)."

### Structure

```python
class Node:
    key, value, prev, next          # key stored so eviction can delete from dict

class LRUCache:
    max_capacity
    lookup       = {}               # key -> Node
    head, tail   = Node(), Node()   # sentinels, head.next = LRU, tail.prev = MRU
```

Primitives — all unlink/relink logic lives here, nowhere else:

- `_detach(node)` → two unconditional pointer writes.
- `_append(node)` → insert just before `self.tail`.
- `_move_to_back(node)` → `_detach` + `_append`; early-return if already `self.tail.prev`.
- `_pop()` → if `self.head.next is not self.tail`: delete `node.key` from dict, `_detach(node)`.

### The three paths in `put`

1. **Existing key** → `_move_to_back`, then update `node.value`. (Three logical paths, but 2 and 3 collapse into one branch with a conditional eviction — say that.)
2. **New key, room available** → create, add to dict, `_append`.
3. **New key, at capacity** → `_pop()` first, then as above.

### Pitfalls avoided

- **Orphaned nodes on update.** Unconditionally building a new `Node` on `put` leaves the old one in the list while the dict points elsewhere — list and dict silently diverge and capacity drifts.
- **Forgetting the back pointer.** Every unlink is _two_ writes. Routing all eviction through `_detach` makes this impossible to get wrong in one caller and right in another.
- **Truthiness on objects.** `if not node` and `node == other` work only because `Node` defines no `__bool__`/`__eq__`. Use `if node is None` and `is` / `is not` — they say what you mean and survive someone adding `__eq__` later.
- **A `peek` helper that reads `dict.keys()`.** That's insertion order and tells you nothing about recency — it will pass while your LRU ordering is completely wrong. Walk the list instead.
- **Annotation-only attributes.** `self.prev: Node` with no assignment doesn't create the attribute. Fine if `_append` always runs first, but say so deliberately.

### Follow-ups to have loaded

- _Does a miss count as an access?_ No — a miss touches nothing.
- _Why `==` on the capacity check?_ The invariant guarantees the dict never exceeds capacity, so it's sufficient; `>=` is defensive and free.
- _What if eviction is called on an empty cache?_ Guarded by `self.head.next is not self.tail`.

---

## Part 2 — Access counts and priority

`get_count(key)`; return the highest-priority key in O(log n), priority = access count, ties broken by most-recently-used; **discuss keeping the priority structure consistent as counts change** ← this is the graded bullet.

### Clarifying questions

Part 1's questions were about behaviour. Part 2's are about **interactions between features** — that's where underspecified prompts hide ambiguity.

- Does `put` increment the count, or only `get`? → **Only `get`.** `put` bumps recency only.
- Does a miss increment? → No.
- Does a count survive eviction and re-insertion? → **No, resets to 0.** (Storing the count on the node silently chooses this — choose it deliberately.)
- Is the priority query a peek or a pop? → **Peek**, must not mutate the cache.
- May I import `heapq`? → Narrate it: _"min-heap, so I'll negate the counts. Happy to hand-roll sift-up/sift-down, but I'd rather spend the time on staleness handling since that's the real complexity."_
- `get_count` on a missing key? → **0**: honest, keeps the return type `int` so callers can do arithmetic, matches `Counter` semantics. Counterargument to name: 0 conflates "absent" with "present but never read."

### Design

- **`count` on the node** → `get_count` is O(1) via the existing dict.
- **Max-heap for priority.** Say why not a BST: you only need the extreme element, not ordered traversal or range queries, so a BST charges you rebalancing for capability you don't use. A heap keeps the max at the root.
- **Immediately name the heap's weakness:** it's only _partially_ ordered, so locating an arbitrary key is O(n). It cannot support "find key `b` and change its priority." _(Vocabulary: heaps **sift**, they never rebalance — don't hand back the distinction you just drew.)_
- **Recency as a comparable value.** Recency is currently _position in a list_, so comparing two arbitrary nodes is O(n). Add a **monotonic integer `tick`** on the cache, incremented on every recency-affecting action, stamped onto the node. Not `time.time()`: one-second resolution means same-second collisions, and NTP can move the clock backward, inverting your ordering. _(Good aside: a real TTL requirement would flip you back to wall-clock — different job.)_

### The tick / count matrix

|Action|`count`|`tick`|
|---|---|---|
|`get` hit|++|++|
|`get` miss|—|—|
|`put` on existing key|—|++|
|`put` new key|—|++ (initial stamp)|

Getting this wrong makes the tiebreak silently disagree with eviction order — a bug no casually-written test catches.

### The heap entry

```python
(-node.count, -node.tick, key)
```

- `-count` first: negation gives max behaviour from a min-heap.
- `-tick` second: consulted only when counts tie; larger tick → more negative → wins.
- `key` last: identifies the entry. Never reached for comparison, since keys are unique.

**Push a frozen tuple, never the node.** Nodes are mutable: if the object in the heap array changes its own priority without moving, the invariant is violated and nothing can detect it. A tuple can go _stale_, which is detectable; a mutated node _corrupts_, which isn't. (`Node` also defines no `__lt__`, so `heapq` would raise `TypeError` — but the mutability argument is the real one, and it applies just as much to a hand-rolled heap.)

**The tick must be inside the tuple.** "The dict gives me O(1) access to the tick" doesn't help — the heap does its comparisons internally during sift and can't consult your dict. With `(-count, key)`, ties break lexicographically by key: `"apple"` beats `"zebra"` regardless of recency. Silently wrong, passes casual tests.

### The two families (this is the graded discussion)

**Eager — indexed heap.** Maintain a side dict `key → index in the heap array`, updated inside `_swap` so every sift keeps it current. Locating a key becomes O(1), repositioning O(log n), so increment-priority is a true O(log n). Heap size never exceeds capacity; eviction removes eagerly. _This is the same move as Part 1: pair a structure that's fast at its job but can't locate elements with one that can._ Cost: `heapq` can't do it (it doesn't expose swaps), so ~40 lines of fiddly bookkeeping that's easy to get subtly wrong under time pressure.

**Lazy — deletion on read.** Never update; push a fresh snapshot on every access and let old entries rot. Filter at query time.

```python
def highest_priority(self):
    while self.heap:
        neg_count, neg_tick, key = self.heap[0]
        node = self.lookup.get(key)
        if node is not None and node.count == -neg_count and node.tick == -neg_tick:
            return key              # snapshot matches live state
        heapq.heappop(self.heap)    # fossil — discard
    return None
```

Cost: heap grows with the number of _accesses_, not keys — O(A) space, unbounded. Query is amortized O(log n) but can burst.

**The line for the room:** _"Lazy, because it's stdlib and I can get it correct in the time we have. If this were production with high read volume or bounded memory, I'd build the indexed heap so the heap stays bounded by capacity."_ Naming the tradeoff **and the condition that flips it** is what's being graded. Picking lazy silently looks like you didn't know the alternative existed.

### Pitfalls avoided

- **Validating only key-existence.** Key `x` is accessed 50 times, evicted, re-inserted, accessed once. Root claims `(-50, ..., "x")`; `x` _is_ in the dict, so a membership-only check returns a count of 50 when the truth is 1. **Validate the whole snapshot** — key present _and_ count matches _and_ tick matches.
- **Checking count but not tick.** `put` on an existing key bumps tick without bumping count, so an entry can carry the right count and a stale tick — quietly breaking the tiebreak.
- **Traversing children to skip a stale root.** Don't. `heappop` the fossil: that promotes the last element, sifts down, and re-establishes a valid root in O(log n). Traversing siblings isn't O(log n) and leaves the fossils in place to be paid for again on every future query.
- **Assuming eviction must purge the heap.** Under lazy, eviction does **nothing** to the heap — O(1). Staleness is caught at query time by the `node is None` branch.

### Why discarding fossils is safe (have this ready)

A fossil can never be the answer: either its key is gone, or the live node has since moved to a _better_ position, meaning a newer, truer entry for that same key sits deeper in the heap. Discarding never discards a candidate. Amortized O(log n), since each entry is pushed once and popped at most once.

---

## Part 3 — Expiry (TTL)

`put(key, value, ttl)`; `get` on an expired entry is a miss and removes it; **expired entries must not count toward capacity**; justify lazy vs active eviction.

### Clarifying questions

- TTL relative or absolute? → Relative seconds in; **store the absolute expiry**.
- Does `put` on an existing key refresh the TTL? → Your call, but say which — it's what creates fossils in the expiry heap.
- Is `ttl` optional / can entries be immortal? → Yes, `ttl=None`. Handle it.
- Does an expired entry's count survive re-insertion? → Be consistent with Part 2 (no).

### Lead with what breaks

**Your capacity check is now wrong.** `len(self.lookup) == self.max_capacity` counts expired-but-untouched entries, but the spec says they mustn't count toward capacity.

**And the second bug behind it:** `_pop()` evicts `self.head.next`, the least _recently used_ node. Recency order and expiry order are independent, so you can evict a live entry while three expired ones sit in the middle still occupying capacity. **Eviction and expiry select different victims.**

Order of operations in `put`: **purge expired → check capacity → evict LRU if still full.**

### Keep both clocks

- **`tick`** (monotonic counter) — ordering and identity: recency tiebreak, snapshot staleness. Unique by construction, never moves backward.
- **`expires_at`** (wall-clock) — TTL semantics, because "30 seconds" must mean 30 real seconds. (`time.monotonic()` is the better clock if expiries never need to cross process boundaries or be logged.)

Different jobs, different fields. A wall-clock stamp cannot do the tick's job: two accesses in the same second collide.

### Second min-heap, keyed by expiry

Entries: `(expires_at, key)`. Not the priority heap — priority order and expiry order are unrelated. Immortal entries (`ttl=None`) are simply never pushed.

Same staleness pattern, **higher stakes**: in Part 2 acting on a fossil discards a candidate (harmless); here acting on one **deletes a live key** (data loss). Validate before mutating.

The purge loop has three branches, and the middle one is what makes it cheap:

- **Fossil** — entry's `expires_at` disagrees with `node.expires_at`, or key absent → pop, continue, **don't touch the node**.
- **Valid and not yet expired** → **stop.** It's a min-heap; if the root isn't expired, nothing is.
- **Valid and expired** → delete from dict, `_detach`, pop, continue.

### The hole in pure lazy-on-access

Full cache, every entry expired, nobody calls `get`, a `put` arrives for a new key. Nothing ever inspects those entries. **So the purge must also be triggered from `put`, before the capacity check.**

Complexity: purging _k_ entries is **O(k log n)** — each removal is a heappop, not constant-time. Worst case _k_ = n, so a single `put` can be **O(n log n)**. **Amortized O(log n)** per operation, since each entry is pushed to the expiry heap once and popped at most once.

That gap is also the honest case _for_ a sweeper: amortized bounds are cold comfort when the pathological `put` lands on a latency-sensitive request. That's a **tail-latency** argument — more precise than "keeps the hot path clean."

### Lazy vs active sweeper

Sweeper costs: a `threading.Thread` with a sleep loop (no async needed); locks around every mutation, since dict, list, and both heaps must move together or a reader observes a node detached from the list but still in the dict; a wake interval that's either too coarse (expired entries linger, capacity wrong in between) or too fine (CPU burn on an idle cache); lock contention on a hot cache; thread lifecycle and leaks.

**The answer that lands — the hybrid, which is what production caches do.** Lazy purge as the _correctness_ mechanism, plus an optional **bounded** sweep ("purge at most 20 per call," or sample every _n_ seconds) as a latency smoother. Correctness never depends on the sweeper running, so it can be added later without touching invariants. Redis works roughly this way: lazy expiry on access plus a sampled background pass.

> _"Lazy for correctness — simple, can't get out of sync. If we measured p99 spikes from bulk purges, I'd add a bounded incremental sweep. But I'd want that number before adding a thread and locks to a structure with four coupled internal states."_

Justifying with a **measurement you'd take** rather than a guess is the senior-sounding version.

### Cross-part interaction to raise unprompted

`highest_priority` can return an expired key, which must behave as absent. **Don't patch it** — purge first, and the existing `node is None` branch catches it for free. Same for `get`, `put`, and `get_count`: **purge-then-act**, stated once as a principle.

---

## Part 4 — Thread safety

### The trap in the prompt

It invites you to compare a **read-write lock** under a read-heavy workload. Answer the prior question first:

**Is `get` a read? No.** It bumps `count` and `tick`, relinks a node, and pushes to the priority heap. **There are no read-only operations in this cache — every caller is a writer.** So an RWLock delivers _zero_ parallelism here while adding complexity and overhead, even at 95% reads. Naming that explicitly is worth more than any code in this part.

### What to ship

**A single `threading.RLock`, acquired at the entry of every public method.** Private helpers (`_detach`, `_append`, `_purge_expired`) are lock-free and assume the lock is held.

Why reentrant: public methods call each other — `put` and `get` both need the purge routine. If that routine acquires the lock itself and `put` already holds it, a plain `Lock` self-deadlocks. Two fixes: `RLock`, or the discipline that only public methods acquire. The second is cleaner and cheaper; `RLock` is more forgiving under time pressure. Say which and why — and mention the lock-free-internals layering.

**Why not finer-grained, precisely:** the GIL means only one thread executes Python bytecode at a time. Fine-grained locking pays off only when threads do real work in parallel, which needs I/O or a C extension that releases the GIL. Your critical sections are pointer swaps and dict writes — pure bytecode, microseconds, no GIL release. Splitting buys ~no throughput and adds lock-ordering discipline, deadlock risk, and torn reads. Note the GIL protects individual bytecodes, **not multi-step invariants** — it is not a substitute for the lock.

**The deeper reason:** _your invariants span all four internal structures, so your critical section must too._

### The two failures a split would hit

- **Deadlock.** `get` takes data→heap while `highest_priority` takes heap→data; two threads each hold one and wait forever. Fixable with a global lock ordering, but that's an invisible rule every future change must honour — which is how real codebases acquire deadlocks years later.
- **Torn reads.** `highest_priority` peeks the heap root, then validates against `node.count`/`node.tick`. Release the heap lock in between and another thread's `get` bumps that node — you're now comparing against state that didn't exist when the root was read. You reject a valid entry, or accept a stale one. The validation is only meaningful if the peek and the node read are atomic.

### Two sharp additions

- **Free-threaded Python (3.13+, PEP 703) changes the calculus.** No GIL means fine-grained locking starts to matter. Honest framing: _"single lock is right for CPython today; on a free-threaded build, or porting to a language without a GIL, I'd revisit."_
- **The scaling answer isn't finer locks — it's sharding.** Partition into N independent caches by `hash(key) % N`, each with its own lock; contention drops ~N-fold with no cross-shard ordering to get wrong. The catch: global operations (`highest_priority`, total capacity) lose a single consistent view. Name that rather than pretending sharding is free.

> _"Single `RLock` across each public method, lock-free helpers. The cache has four coupled internal structures and every operation touches at least two, so the lock has to cover the whole thing; under the GIL a finer split adds risk without throughput. If profiling showed lock contention as the bottleneck, I'd shard before splitting locks."_

---

## Delivery notes

- **Never start with silence.** The named reject signal is going quiet for five minutes and then jumping straight to code. Design first: structures, why, failure modes of the alternatives, edge-case strategy, complexity.
- **State complexity unprompted** at the end of every design statement. Getting it on the record before you're asked reads as confidence.
- **Volunteer your edge-case strategy.** Boundary-condition handling is explicitly graded. Say the sentinel plan out loud as part of the design, not when asked.
- **Drop the hedging.** One clause, once: _"Heaps aren't something I reach for daily, so let me reason through it out loud."_ That's calibration. "Bear with me, I expect this to be rocky, sorry" is pre-apologising for work you then do correctly.
- **Narrate imports rather than requesting permission.** "`OrderedDict` does exactly this, I'll build it by hand" > "am I allowed to use `OrderedDict`, it'd solve a lot of this for me."
- **Deferrals count only if spoken.** "I'm skipping input validation, flagging it" reads completely differently from just not doing it.
- **Outline your tests even if you don't write them.** Eviction order, update-existing-key, capacity 1, repeated gets on one key, expired-entry-doesn't-count-toward-capacity. Make any debug helper walk the list, not `dict.keys()`.
- **Getting stuck is not failure; how you respond to a hint is a first-class signal.** Stay talking. Freezing, going silent, or getting defensive scores worse than a wrong turn you narrate.
- **A stated-and-scoped shortcut earns most of the credit.** "Let me get this correct with an O(n) scan, then optimize — the fix is a binary heap: push appends and sifts up, pop moves the last element to the root and sifts down." Precise about the fix beats silent stalling.
- **Reserve the last 10–15 minutes for testing and refactoring** rather than typing flat out.