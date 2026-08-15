---
tags:
  - programming-language
  - python
  - iterator
  - design-patterns
---
# Iterators
As you'd expect, a python iterator is a protocol which implements the iterator design pattern, which can be used to iterate over a collection of items (`list`, `dict`, `tuple`, etc).

The responsibility of an iterator is to -
* Return one item from the container at a time
* Keep track of current and visited items

In python, they're implemented using a standard well known iterface (or `Protocol` in python) using the `.__iter__()` and `.__next__()` methods.

| Method        | Description                                                                                                                                                        |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `.__iter__()` | Called to initialize the iterator. It must return an iterator object. Typically returns `self`.                                                                    |
| `.__next__()` | Called to iterate over the iterator. It must return the next value in the data stream. When no items are left in the container, raise a `StopIteration` exception. |
Iterators are most useful when you have a need to iterate over an unknown amount, or huge number of items from something like a database, over the network, or off your local filesystem. In these situations, iterators allow you to process collections one item at a time without exhausting all local resources of your system.
## Standard example
Here is an iterator that returns the original item from the collection -
```python
from collections.abc import Iterator, Sequence


class SequenceIterator[T]:
	def __init__(self, sequence: Sequence[T]) -> None:
		self._seq = sequence
		self._idx = 0
		
	def __iter__(self) -> Iterator[T]:
		return self
		
	def __next__(self) -> T:
		if self._idx < len(self._seq):
			item = self._seq[self._idx]
			self._idx += 1
			return item
		else:
			raise StopIteration
```
You can also just inherit from `collections.abc.Iterator` to easily create custom iterators -
```python
from collections.abc import Iterator, Sequence


class SequenceIterator[T](Iterator[T]):
    def __init__(self, sequence: Sequence[T]) -> None:
        self._seq: Sequence[T] = sequence
        self._idx: int = 0

    def __next__(self) -> T:
        if self._idx < len(self._seq):
            item = self._seq[self._idx]
            self._idx += 1
            return item
        else:
            raise StopIteration
```
## Transformer example
Here is an example that will return the value squared from the collection -
```python
from collections.abc import Iterator, Sequence


class SquaredIterator[int]:
	def __init__(self, sequence: Sequence[int]) -> None:
		self._seq = sequence
		self._idx = 0
		
	def __iter__(self) -> Iterator[int]:
		return self
		
	def __next__(self) -> int:
		if self._idx < len(self._seq):
			item = self._seq[self._idx]**2
			self._idx += 1
			return item
		else:
			raise StopIteration
```
## Generating new data example
You need to necessarily wrap a simple data structure -
```python
from collections.abc import Iterator

class FibonacciIterator[int]:
    def __init__(self, stop: int = 10) -> None:
        self._stop = stop
        self._idx = 0
        self._curr = 0
        self._next = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self._idx < self._stop:
            self._idx += 1
            fib_number = self._curr
            self._curr, self._next = (
                self._next,
                self._curr + self._next,
            )
            return fib_number
        else:
            raise StopIteration
```
## Doing it Async
Async iterators are conceptually the same, but with a few key differences you need to remember! They have different magic methods you need to implement, which are just an "async" flavor of the original ones, and there is an async flavor of `StopIteration` (`StopAsyncIteration`).

| Sync                  | Async                      |
| --------------------- | -------------------------- |
| `__iter__` -> `self`  | `__aiter__` -> `self`      |
| `__next__`            | `async def __anext__`      |
| `raise StopIteration` | `raise StopAsyncIteration` |
| `for x in it`         | `async for x in it`        |
```python
import asyncio

class AsyncCounter:
	def __init__(self, limit: int) -> None:
		self._limit = limit
		self._i = 0
		
	def __aiter__(self) -> "AsyncCounter":  # Note: NOT ASYNC
		return self
		
	async def __anext__(self) -> int:
		if self._i >= self._limit:
			raise StopAsyncIteration
			
		await asyncio.sleep(0.01)
		self._i += 1
		return self._i
		
		
async def main() -> None:
	async for n in AsyncCounter(3):
		print(n)
		
		
asyncio.run(main())
```

There are some gotchas worth knowing.
- `StopIteration` inside a coroutine does not end the loop - it becomes a `RuntimeError`. Python deliberately blocks it because `StopIteration` already has a meaning inside generators.
- There is no built-in `anext()` before Python 3.10 you can call `await anext(it)` and `await anext(it, default)`; below that, `await it.__anext__()` directly.