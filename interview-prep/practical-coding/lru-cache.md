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
## Part B - TTL
Entries expire N seconds after insert. Lazy expiry on access vs. background sweeper - implement lazy, discuss sweeper.
## Part C - Thread safety
Wrap operations in a lock; discuss why `get` also mutates (recency update) so even reads need the write lock; mention lock-free/sharded designs as the scale answer.