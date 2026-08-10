# Implement a doubly linked list.
#
# Reps to practice:
# * track head, tail, and length
# * add a node at the head
# * add a node at the tail
# * insert a node at an arbitrary index, including the middle
# * keep both next and prev pointers correct after every mutation
# * handle empty lists and invalid indexes cleanly
class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.prev: Node | None = None
        self.next: Node | None = None


class DoublyLinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None
        self.tail: Node | None = None
        self._length = 0

    def __len__(self) -> int:
        raise NotImplementedError

    def append_head(self, value: int) -> None:
        raise NotImplementedError

    def append_tail(self, value: int) -> None:
        raise NotImplementedError

    def insert_at(self, index: int, value: int) -> None:
        raise NotImplementedError

    def to_list(self) -> list[int]:
        raise NotImplementedError

    def to_list_reverse(self) -> list[int]:
        raise NotImplementedError
