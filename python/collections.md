---
tags:
  - collections
  - programming-language
  - python
---
# Collections
Notes regarding python's `collections` module
## Overview
The `collections` module implements several specialized container types which
can be used in-place of the built-in `dict`, `list`, `set`, and `tuple` types.
### Counter
A `dict` subclass mapping items to counts. Missing keys return `0` instead of raising - but unlike `defaultdict`, reading a missing key does not insert it.
```python
from collections import Counter

c = Counter("mississippi")     # counts characters
c = Counter(["a", "b", "a"])   # counts list items
c = Counter({"a": 2, "b": 1})  # from a mapping
c = Counter(a=2, b=1)          # from kwargs

c["z"]                         # 0, and z is still not in c
c["a"] += 1                    # works from nothing; no initialization needed
```
#### Core operations
```python
c.most_common()                  # [(item, count), ...] descending
c.most_common(3)                 # top 3 - this is a heap internally, cheaper than sorting
c.total()                        # sum of counts (3.10+); else sum(c.values)
c.elements()                     # iterator repeating each item count times
c.update(other)                  # ADDS counts (dict.update would overwrite)
c.subtract(other)                # subtracts; CAN go negative
c.values(), c.keys(), c.items()  # normal dict apis
+c                               # strips zero and negative counts
```
Update rather than replacing is the behavioral difference from `dict` that is worth remembering.
#### Multiset arithmatic
```python
a, b = Counter("aab"), Counter("abc")

a + b  # Counter({'a': 3, 'b': 2, 'c': 1}) - sums
a - b  # Counter({'a': 1}) - DROPS zero/negative
a & b  # Counter({'a': 1, 'b': 1}) - min of each (intersection)
a | b  # Counter({'a': 2, 'b': 1, 'c': 1}) - max of each (union)
```
`a - b` silently discarding negatives is a gotcha, use `a.subtract(b)` to keep them.
#### Patterns
```python
# anagram check
Counter(s1) == Counter(s2)

# is d1 a sub-multiset of s2?
not (Counter(s1) - Counter(s2))

# most common word
Counter(re.findall(r"\w+", text.lower())).most_common(1)[0]

# frequency of frequencies
Counter(Counter(items).values())

# group sizes without defaultdict
Counter(len(g) for g in groups)
```
#### Gotchas
- `most_common()` ties are in insertion order - not sorted, and not stable across differently built counters.
- Counts can be negative or non-integer if you set them manually; most methods still work but `elements()` skips anything <= 0.
- Equality is `dict` equality: `Counter(a=1) == Counter(a=1, b=0)` is `False`. Use `+c` to normalize first.
### deque
A doubly-linked-ish structure with **O(1) appends and pops at both ends**. A list is O(1) at the right end and O(n) at the left, because every `pop(0)` shifts the whole array. Thats the entire reason `deque` exists, it has O(1) performance in either direction.

As such, it's a pretty good thing to reach for when you need a stack or queue.
```python
from collections import deque

dq = deque([1, 2, 3])
dq.append(4)      # right
dq.appendleft(0)  # left
dq.pop()          # 4, from right
dq.popleft()      # 0, from left
```
#### Full API
```python
# The full API
dq.extend([4, 5])       # right
dq.extendleft([0, -1])  # left - NOTE: reverses, ends up [-1, 0, ...]
dq.rotate(1)            # right by 1: last element moves to the front
dq.rotate(-1)           # left
dq.clear()
dq[0], dq[-1]           # O(1)
dq[len(dq)//2]          # O(n) - indexing in the middle is slow
```
`extendleft` reversing its input surprises everyone at least once :).
#### maxlen - the killer feature
```python
window = deque(maxlen=3)
for x in [1, 2, 3, 4, 5]:
	window.append(x)  # appending past maxlen auto-drops from the other end
list(window)          # [3, 4, 5]
```
Free sliding window, free "last N events" ring buffer, no book keeping. `dq.maxlen` is readable, not settable.
#### Patterns
```python
# BFS - the canonical use
q = deque([start])
while q:
	node = q.popleft()
	q.extend(neighbors(node))
	
# sliding window maximum - store indices, keep values decreasing
dq = deque()
for i in enumerate(nums):
	while dq and nums[dq[-1]] <= x:
		dq.pop()
	dq.append(i)
	if dq[0] <= i - k:
		dq.popleft()
	# nums[dq[0]] is the max of the current window
	
# LRU-ish recent history
recent = deque(maxlen=100)
```
#### Gotchas
- Middle indexing is O(n). Not a random access structure.
- No slicing. `dq[1:3]` raises `TypeError`. Use `itertools.islice(dq, 1, 3)`.
- `deque` is thread safe for appends (not a gotcha, but good trivia to know).
- `dq.remove(x)` and `x in dq` are both O(n)
## Further Reading
[docs][docs]
[docs]:https://docs.python.org/3/library/collections.html "https://docs.python.org/3/library/collections.html"