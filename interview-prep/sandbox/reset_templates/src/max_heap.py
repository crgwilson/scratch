# Implement a max heap backed by a Python list.
#
# Reps to practice:
# * map parent and child indexes correctly
# * push by appending and sifting up
# * pop by moving the tail to the root and sifting down
# * preserve the heap invariant with duplicates, negatives, and single-item heaps
# * return None from peek/pop on an empty heap
class MaxHeap:
    def __init__(self, values: list[int] | None = None) -> None:
        self.heap: list[int] = []

    def __len__(self) -> int:
        raise NotImplementedError

    def push(self, value: int) -> None:
        raise NotImplementedError

    def peek(self) -> int | None:
        raise NotImplementedError

    def pop(self) -> int | None:
        raise NotImplementedError

    def _sift_up(self, index: int) -> None:
        raise NotImplementedError

    def _sift_down(self, index: int) -> None:
        raise NotImplementedError
