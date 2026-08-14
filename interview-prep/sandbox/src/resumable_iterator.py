"""P2 - Resumable Iterator.

Implement Parts B and C without changing the public method signatures.

Part A lives in tests/test_resumable_iterator.py: write one reusable contract
test that can validate either implementation.

Part B: implement ResumableListIterator.

Part C: implement ResumableMultiFileIterator. Assume ResumableFileIterator is
provided and conforms to the ResumableIterator interface. It accepts one path
and yields the records in that JSON-lines file. For local practice, the tests
replace it with ResumableListIterator and use lists as the "files."

Part D (stretch): sketch or implement an async multi-file version and consider
what checkpoint means while a read is in flight.
"""

from typing import Any, Generic, TypeVar


T = TypeVar("T")

class ResumableIterator(Generic[T]):
    def __iter__(self) -> "ResumableIterator[T]":
        return self

    def __next__(self) -> T:
        raise NotImplementedError

    def checkpoint(self) -> Any:
        """Return an opaque object representing the next element to yield."""
        raise NotImplementedError

    def resume(self, state: Any) -> None:
        """Restore a state previously returned by this iterator type."""
        raise NotImplementedError


class ResumableListIterator(ResumableIterator[T]):
    def __init__(self, items: list[T]) -> None:
        raise NotImplementedError


class ResumableMultiFileIterator(ResumableIterator[Any]):
    def __init__(self, paths: list[str]) -> None:
        raise NotImplementedError
