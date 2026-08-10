from max_heap import MaxHeap


def assert_max_heap_property(heap: list[int]) -> None:
    for index, value in enumerate(heap):
        left = (index * 2) + 1
        right = (index * 2) + 2
        if left < len(heap):
            assert value >= heap[left]
        if right < len(heap):
            assert value >= heap[right]


def test_empty_heap_peek_and_pop_return_none() -> None:
    heap = MaxHeap()

    assert len(heap) == 0
    assert heap.peek() is None
    assert heap.pop() is None


def test_push_maintains_max_heap_property() -> None:
    heap = MaxHeap()

    for value in [1, 2, 4, 5, 6, 9]:
        heap.push(value)
        assert_max_heap_property(heap.heap)
        assert heap.peek() == max(heap.heap)

    assert len(heap) == 6


def test_pop_returns_values_from_largest_to_smallest() -> None:
    heap = MaxHeap()
    values = [3, 1, 8, 5, 2, 8, -4, 0]

    for value in values:
        heap.push(value)

    popped = []
    while len(heap) > 0:
        popped.append(heap.pop())
        assert_max_heap_property(heap.heap)

    assert popped == sorted(values, reverse=True)
    assert heap.pop() is None


def test_single_item_heap_can_be_popped() -> None:
    heap = MaxHeap()

    heap.push(42)

    assert heap.peek() == 42
    assert heap.pop() == 42
    assert len(heap) == 0
    assert heap.peek() is None


def test_constructor_can_heapify_initial_values() -> None:
    heap = MaxHeap([4, 10, 3, 5, 1])

    assert len(heap) == 5
    assert heap.peek() == 10
    assert_max_heap_property(heap.heap)
    assert [heap.pop() for _ in range(5)] == [10, 5, 4, 3, 1]
