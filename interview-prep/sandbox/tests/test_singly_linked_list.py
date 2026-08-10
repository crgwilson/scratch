import pytest

from singly_linked_list import SinglyLinkedList


def test_new_list_starts_empty() -> None:
    linked_list = SinglyLinkedList()

    assert len(linked_list) == 0
    assert linked_list.to_list() == []
    assert linked_list.head is None


def test_append_head_adds_to_empty_list() -> None:
    linked_list = SinglyLinkedList()

    linked_list.append_head(10)

    assert len(linked_list) == 1
    assert linked_list.to_list() == [10]
    assert linked_list.head is not None
    assert linked_list.head.value == 10
    assert linked_list.head.next is None


def test_append_head_adds_before_existing_head() -> None:
    linked_list = SinglyLinkedList()

    linked_list.append_head(2)
    linked_list.append_head(1)
    linked_list.append_head(0)

    assert len(linked_list) == 3
    assert linked_list.to_list() == [0, 1, 2]


def test_append_tail_adds_to_empty_and_non_empty_list() -> None:
    linked_list = SinglyLinkedList()

    linked_list.append_tail(1)
    linked_list.append_tail(2)
    linked_list.append_tail(3)

    assert len(linked_list) == 3
    assert linked_list.to_list() == [1, 2, 3]


def test_insert_at_head_middle_and_tail() -> None:
    linked_list = SinglyLinkedList()
    linked_list.append_tail(1)
    linked_list.append_tail(3)
    linked_list.append_tail(5)

    linked_list.insert_at(0, 0)
    linked_list.insert_at(2, 2)
    linked_list.insert_at(5, 6)

    assert len(linked_list) == 6
    assert linked_list.to_list() == [0, 1, 2, 3, 5, 6]


def test_insert_at_rejects_invalid_indexes_without_mutating() -> None:
    linked_list = SinglyLinkedList()
    linked_list.append_tail(1)
    linked_list.append_tail(2)

    with pytest.raises(IndexError):
        linked_list.insert_at(-1, 99)

    with pytest.raises(IndexError):
        linked_list.insert_at(3, 99)

    assert len(linked_list) == 2
    assert linked_list.to_list() == [1, 2]
