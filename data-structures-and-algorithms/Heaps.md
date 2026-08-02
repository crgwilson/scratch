A heap is a binary tree represented as a flat array, as such the height of the heap will be O(logN), but it is best used to fetch the largest or smallest element in a collection.

There are both min and max heaps, min heaps are good for finding the smallest value, max heaps are good for finding the largest.

Focusing on a max heap for now -

* Getting the max (peek) is O(1) since the max will be the root element.
* Inserting a new element (push) is O(logN) as "sifts" up the height of the tree (in the worst case).
* Removing the max (pop) is also O(logN) because you need to move the last element to the root and then "sift" down.
* Building a max heap from an array is O(N)
* Searching for an arbitrary value in a max heap is O(N)

With heaps, you never actually build the tree with nodes, you use a flat list and simulate the tree using index arithmetic.
* Parent of index `i` is `(i-1) // 2`
* Left child of index `i` is `2i+1`
* Right child of index `i` is `2i+2`
For example, the list `[9, 5, 6, 1, 4, 2]` represents this tree:

```
            9(0)
          /      \
       5(1)      6(2)
      /    \      /
   1(3)   4(4)  2(5)
```

Full impl -
```python
class MaxHeap:
    def __init__(self):
        self.heap = []

    def push(self, val):
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def peek_max(self):
        return self.heap[0] if self.heap else None

    def pop_max(self):
        if not self.heap:
            return None
        top = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return top

    def _sift_up(self, i):
        parent = (i - 1) // 2
        while i > 0 and self.heap[i] > self.heap[parent]:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            i, parent = parent, (parent - 1) // 2

    def _sift_down(self, i):
        n = len(self.heap)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            largest = i
            if left < n and self.heap[left] > self.heap[largest]:
                largest = left
            if right < n and self.heap[right] > self.heap[largest]:
                largest = right
            if largest == i:
                break
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            i = largest
```

`push` adds a new element
```python
def push(self, val):
	self.heap.append(val)
	self._sift_up(len(self.heap) - 1)
```
We always add a new element to the end of the array, but it probably doesn't belong there given max-heap ordering, so we need to "sift-up" to put it in its proper place. This means, swapping it with its parent until it's no longer bigger than the parent.
```python
def _sift_up(self, i):
	parent = (i - 1) // 2
	while i > 0 and self.heap[i] > self.heap[parent]:
		self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
		i, parent = parent, (parent - 1) // 2
```

`pop_max` removes the largest element
```python
def pop_max(self):
    if not self.heap:
        return None
    top = self.heap[0]
    last = self.heap.pop()
    if self.heap:
        self.heap[0] = last
        self._sift_down(0)
    return top
```
We remove the root (index 0) which will be the largest item in the array, and replace it with the last item. Then we "sift-down" meaning, we replace this new root with its children until it is no longer smaller than any children.
```python
def _sift_down(self, i):
    n = len(self.heap)
    while True:
        left, right = 2 * i + 1, 2 * i + 2
        largest = i
        if left < n and self.heap[left] > self.heap[largest]:
            largest = left
        if right < n and self.heap[right] > self.heap[largest]:
            largest = right
        if largest == i:
            break
        self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
        i = largest
```



My full impl that I almost one-shot -
```python
# Try writing a max heap, should be fun!
#
# Tips -
# * Parent is (i-1) // 2
# * Children are 2i+1 & 2i+1
class MaxHeap:
    def __init__(self) -> None:
        self.heap = []

    def push(self, value: int) -> None:
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)

    def peek(self) -> int | None:
        if self.heap:
            return self.heap[0]
        return None

    def pop(self) -> int | None:
        if not self.heap:
            return None

        root = self.heap[0]
        tail = self.heap.pop()
        if self.heap:
            self.heap[0] = tail
            self._sift_down(0)

        return root

    def _sift_up(self, i: int) -> None:
        # Move the element up, until it is no longer larger
        # than its parent.
        while True:
            if i == 0:
                # We're already at the top, no higher to go.
                break

            parent = (i - 1) // 2
            if self.heap[parent] > self.heap[i]:
                # Parent is larger than the child, so stop sifting up.
                break

            tmp = self.heap[parent]
            self.heap[parent] = self.heap[i]
            self.heap[i] = tmp
            i = parent

    def _sift_down(self, i: int) -> None:
        # Move the element down, until it is no longer smaller
        # than its children.
        while True:
            left = (i * 2) + 1
            right = (i * 2) + 2
            largest = i

            if left < len(self.heap) and self.heap[left] > self.heap[i]:
                largest = left

            if right < len(self.heap) and self.heap[right] > self.heap[i]:
                if self.heap[right] > self.heap[largest]:
                    largest = right

            if largest == i:
                # Neither child is larger, time to stop!
                return

            tmp = self.heap[largest]
            self.heap[largest] = self.heap[i]
            self.heap[i] = tmp
            i = largest
```