import pytest

from doubly_linked_list import DoublyLinkedList


def assert_links_are_consistent(linked_list: DoublyLinkedList) -> None:
    values_forward = []
    values_backward = []

    node = linked_list.head
    previous = None
    while node is not None:
        assert node.prev is previous
        values_forward.append(node.value)
        previous = node
        node = node.next

    assert previous is linked_list.tail

    node = linked_list.tail
    next_node = None
    while node is not None:
        assert node.next is next_node
        values_backward.append(node.value)
        next_node = node
        node = node.prev

    assert values_forward == linked_list.to_list()
    assert values_backward == linked_list.to_list_reverse()


def test_new_list_starts_empty() -> None:
    linked_list = DoublyLinkedList()

    assert len(linked_list) == 0
    assert linked_list.to_list() == []
    assert linked_list.to_list_reverse() == []
    assert linked_list.head is None
    assert linked_list.tail is None


def test_append_head_updates_head_tail_and_links() -> None:
    linked_list = DoublyLinkedList()

    linked_list.append_head(3)
    linked_list.append_head(2)
    linked_list.append_head(1)

    assert len(linked_list) == 3
    assert linked_list.to_list() == [1, 2, 3]
    assert linked_list.to_list_reverse() == [3, 2, 1]
    assert linked_list.head is not None
    assert linked_list.tail is not None
    assert linked_list.head.value == 1
    assert linked_list.tail.value == 3
    assert_links_are_consistent(linked_list)


def test_append_tail_updates_head_tail_and_links() -> None:
    linked_list = DoublyLinkedList()

    linked_list.append_tail(1)
    linked_list.append_tail(2)
    linked_list.append_tail(3)

    assert len(linked_list) == 3
    assert linked_list.to_list() == [1, 2, 3]
    assert linked_list.to_list_reverse() == [3, 2, 1]
    assert linked_list.head is not None
    assert linked_list.tail is not None
    assert linked_list.head.value == 1
    assert linked_list.tail.value == 3
    assert_links_are_consistent(linked_list)


def test_insert_at_head_middle_and_tail() -> None:
    linked_list = DoublyLinkedList()
    linked_list.append_tail(1)
    linked_list.append_tail(3)
    linked_list.append_tail(5)

    linked_list.insert_at(0, 0)
    linked_list.insert_at(2, 2)
    linked_list.insert_at(5, 6)

    assert len(linked_list) == 6
    assert linked_list.to_list() == [0, 1, 2, 3, 5, 6]
    assert linked_list.to_list_reverse() == [6, 5, 3, 2, 1, 0]
    assert_links_are_consistent(linked_list)


def test_insert_at_rejects_invalid_indexes_without_mutating() -> None:
    linked_list = DoublyLinkedList()
    linked_list.append_tail(1)
    linked_list.append_tail(2)

    with pytest.raises(IndexError):
        linked_list.insert_at(-1, 99)

    with pytest.raises(IndexError):
        linked_list.insert_at(3, 99)

    assert len(linked_list) == 2
    assert linked_list.to_list() == [1, 2]
    assert_links_are_consistent(linked_list)
