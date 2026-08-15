`heapq` is how you work with heaps in python's stdlib.

`heapq` does not give you a heap object - it gives you functions which operate on a plain list, maintaining the invariant `a[i] <= a[2i+1]` and `a[i] <= a[2i+2]`. **CRAIG, YOU FUCKING IDIOT, REMEMBER - IT'S A MIN HEAP ONLY** if you need a max-heap instead, you need to negate your values. `a[0]` is always the smallest, the rest of the list is _not sorted_ printing it will look wrong - that's fine.
```python
import heapq

h = []
heapq.heappush(h, 5)
heapq.heappush(h, 1)
heapq.heappush(h, 3)
h[0]              # 1 -> peek, O(1) no function needed
heapq.heappop(h)  # 1 -> remove and return the smallest, O(log n)
```
## Core operations
```python
heapq.heappush(h, item)      # O(log n)
heapq.heappop(h)             # O(log n), raises IndexError if empty
h[0]                         # peek, O(1)
heapq.heapify([9, 6, 8, 3])  # O(n), in-place, returns None
len(h)                       # size; `if h` for emptiness
```
`heapify` being O(n) matters: building from an existing list is cheaper than N pushes.
```python
h = [5, 1, 3]
heapq.heapify(h)  # in-place, does NOT return the list
```
### Combined Ops (cheaper than doing both)
```python
heapq.heappushpop(h, x)  # push then pop - pop of min(x, h[0])
heapq.heapreplace(h, x)  # pop then push - always pops old min, raises if empty
```
`heappushpop` is the one for _"keep the K largest"_: push, and if the new item is smaller than the current min, it just comes straight back out.
## Max heap
```python
heapq.heappush(h, -value)
largest = heapq.heappop(h)
```
There is no max-heap, so negate.

For tuples, negate the sort key only: `(-priority, item)`. If items aren't comparable, see ties below.
## Tuples and ties
Heap elements compare with a normal tuple comparison - element by element. So the second element gets compared when the priorities tie, and if it's not comparable, you get a `TypeError` at a random moment under load.
```python
heapq.heappush(h, (2, {"a": 1},))
heapq.heappush(h, (2, {"b": 2},))  # TypeError: '<' not supported between dicts
```
The fix is a monotonic tiebreaker, which gives you FIFO ordering within a priority.
```python
from itertools import count

counter = count()
heapq.heappush(h, (priority, next(counter), item))
```
This is the most common heap bug, so remember this!
## Convenience functions
```python
heapq.nlargest(3, items)           # sorted descending
heapq.nsmallest(3, items)          # sorted ascending
heapq.nlargest(3, items, key=len)  # key= supported
heapq.merge(a, b, c)               # lazy iterator over sorted inputs
heapq.merge(a, b, key=fn, reverse=True)
```
`nlargest`/`nsmallest` do not need a heap as an input, any iterable works. For k close to n, just `sorted()`; for `k=1`, `min`/`max`. They're a win in the middle.

`merge` is lazy, so it handles inputs that don't fit into memory - the key-way merge answer.
## Patterns
```python
# top-k largest, streaming, O(n log k) with O(k) memory
h = []
for k in stream:
	if len(h) < k:
		heapq.heappush(h, x)
	else:
		heapq.heappushpop(h, x) # h[0] is the k-th largest at all times
		
# running mediam: max-heap for low half, min-heap for high half
# (low stores negated values)

# lazy deletion - heaps have no remove(); tombstone instead
removed = set()
while h and h[0] in removed:
	heapq.heappop(h)
```
## Gotchas
- Mutating an element in place after pushing corrupts the invariant. Pop and re-push instead.
- `heapify` returns `None` - `h = heapq.heapify(my_list)` is a bug that silently gives you `None`.
- The list is not sorted, only `h[0]` is meaningful.
- `heappop()` on empty raises an `IndexError`, guard against it with `if h:`.