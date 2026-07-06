# Collections

Notes regarding python's `collections` module

## Overview

The `collections` module implements several specialized container types which
can be used in-place of the built-in `dict`, `list`, `set`, and `tuple` types.

### deque

`deque` objects are a generalization of stacks and queues. They provide thread-safe,
memory efficient appends and pops from either end of the `deque` with O(1)
performance in either direction.

The standard `list` object supports similar operations but they're optimized for
fixed-length operations and incur O(n) memory movement costs for both `pop(0)`
and `insert(0, v)` which change both the size and position of the underlying data
structure.

If a `deque` is created without a `maxlen` specified (given as `None`) then it
will grow to an arbitrary length. Otherwise the size of it constrained to the given
length.

## Further Reading

[docs][docs]

[docs]:https://docs.python.org/3/library/collections.html "https://docs.python.org/3/library/collections.html"
