Python's `bisect` module provides tools to work with a sorted array. You should reach for it when you want to perform a binary search on a sorted list.

## The mental model
`bisect` essentially has 4 functions you'll be using. `bisect_left`, `bisect_right`, `insort_left`, and `insort_right`. There is also `bisect` and `insort`, but both of these are aliases for their `*_right` counterparts.
```python
from bisect import (
	bisect,
	bisect_right,
	bisect_left,
	insort,
	insort_right,
	insort_left,
)

t = [10, 20, 20, 20, 30]
#     0   1   2   3   4

bisect_left(t, 20)   # 1 -> first index where t[i] >= 20
bisect_right(t, 20)  # 4 -> first index where t[i] > 20
bisect(t, 20)        # same as bisect_right

bisect_left(t, 25)   # 4 -> no equals so both agree
bisect(t, 25)        # 4
```
Basically, left is greater-than or equal, and right is just greater than. Remember that.
## The four boundary queries
This is the part worth memorizing, since almost every problem reduces to one of these.
```python
bisect_left(t, x)       # first i with t[i] >= x
bisect_right(t, x)      # right i with t[i] > x
bisect_left(t, x) - 1   # last i with t[i] < x
bisect_right(t, x) - 1  # last i with t[i] <= x
```
The `- 1` versions can give you `-1` which silently wraps to the end of the list in Python - always guard against it.
```python
i = bisect_right(t, x)
result = t[i - 1] if i else None  # if 'i' is the guard
```
## Recipes
```python
# does x exist?
i = bisect_left(t, x)
found = i < len(t) and t[i] == x

# how many times does x appear?
count = bisect_right(t, x) - bisect_left(t, x)

# all elements in [lo, hi], inclusive both ends
window = t[bisect_left(t, lo) : bisect_right(a, hi)]
```
## Inserting
```python
insort_left(t, x)   # inserts, keeping sorted order
insort_right(t, x)  # same, but after any equals
```
**Important:** the search is O(log n) but the insert is O(n), because it has to shift elements in the list. So inserting is not cheap!
## Tuples and the `key=` parameter
Tuples compare element-by-element, so, for example, a list of `(timestamp, value)` bisects on timestamp naturally:
```python
entries = [(1, "a",), (4, "b",), (9, "c",)]
bisect_right(entries, (4, "b"))  # 2
```
But a problem arises if you want to search by one field without knowing the whole value (i.e. I want to search for 4, but don't know the value of "b"). There are two options:
```python
# Python 3.10+ use key=
bisect_right(entries, 4, key=lambda e: e[0])  # 2

# Any version: sentinel that sorts after anything
bisect_right(entries, (4, chr(0x10FFFF)))     # 2
```

## Things that will bite you
- The list **MUST ALREADY BE SORTED** if it is not, `bisect` will return nonsense.
- Reverse sorted lists **DO NOT WORK**. No `reverse=` parameter exists. For this, either negate your values or sort ascending.
- Bisect works on anything that supports `__getitem__` and `__len__` with comparable elements - including your own class - but not on generators or sets.