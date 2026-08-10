# Implement a binary search tree.
#
# Reps to practice:
# * insert values into the correct subtree
# * search in O(h), where h is the tree height
# * produce an in-order traversal in sorted order
# * find the minimum and maximum values
# * remove leaf nodes, one-child nodes, two-child nodes, and the root
# * ignore duplicate inserts
class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None


class BinarySearchTree:
    def __init__(self) -> None:
        self.root: Node | None = None

    def insert(self, value: int) -> None:
        raise NotImplementedError

    def contains(self, value: int) -> bool:
        raise NotImplementedError

    def inorder(self) -> list[int]:
        raise NotImplementedError

    def min(self) -> int | None:
        raise NotImplementedError

    def max(self) -> int | None:
        raise NotImplementedError

    def remove(self, value: int) -> bool:
        raise NotImplementedError
