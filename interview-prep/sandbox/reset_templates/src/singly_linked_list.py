# Implement a singly linked list.
#
# Reps to practice:
# * track the head pointer and list length
# * add a node at the head
# * add a node at the tail
# * insert a node at an arbitrary index, including the middle
# * handle empty lists and invalid indexes cleanly
#
# Keep append_tail O(n) unless you decide to add a tail pointer as a follow-up.
class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.next: Node | None = None


class SinglyLinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None
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
