# Algorithms

## Big O Time Complexity

Big O categorizes your algorithm's time or memory requirements based on input. It is not meant to be an exact measurement. As your input grows how fast does your computation or memory grow?

For a stupid example, this code...
```typescript
function sum_char_codes(n: string): number {
    let sum = 0;
    for (let i = 0; i < n.length; ++i) {
        sum += n.charCodeAt(i);
    }
    return sum;
}
```
...is **O(N)** as it grows linearly. If the length of input string `n`, increases in length by 50%, our function will take roughly 50% longer since we're looping through it.

Time Complexities

* O(1) constant no matter the input
* O(LogN) binary search trees
* O(N)
* O(NLogN) quicksort
* O(N^2) nested for loop
* O(2^N)
* O(N!)

The logarithm of a number if the number of steps down to 1 in binary, IE log 4096 = 12
```
Start   - 4096
Step 1  - 2048
Step 2  - 1024
Step 3  - 512
Step 4  - 256
Step 5  - 128
Step 6  - 64
Step 7  - 32
Step 8  - 16
Step 9  - 8
Step 10 - 4
Step 11 - 2
Step 12 - 1
```

### Important Concepts

* Look for loops
* Always drop constants IE: O(2N) == O(N)
* Always assume worst case
* If you half at each step, it's likely O(LogN) or O(NLogN)

## Arrays Data Structure

An array is a contiguous memory space which contains a certain amount of bytes.

* Fixed size, cannot grow
* No `insertAt`, or push, or pop

```java
int[] foo = int[3];  // An int array with 3 open slots
foo = {1,2,3};  // Populate the array
System.out.println(foo[2]);  // Get the value at the 2nd index in array `foo`
```

Arrays don't reallocate themselves and dynamically grow / shrink. Therefore you never really "insert" you overwrite, and you never "delete" you null / zero out the index IE: set the value to a sentinel value (falsey).

* Retrieving a value knowing the index is **O(1)**
* Retrieving a value not knowing the index is **O(N)**

### ArrayList

ArrayLists are wrappers on top of arrays which reallocate the underlying array when capacity is reached.

### ArrayBuffer / RingBuffer

An ArrayBuffer uses an array as its underlying data structure, but given an Array of size N, we are not using index 0 as head and N as tail, separate head and tail indicies are tracked. This means we can use this for queue like operations without needing to shift every element in the array. Additionally, ArrayBuffers / RingBuffers / whatever you want to call them maintain element order.

If the array size is exceeded, the tail will wrap around to index 0.

Issues happen when your tail exceeds your head, meaning you need to reallocate and shift the whole data structure.

A good use case for an ArrayBuffer log collection and batched flushing.

## Linear Search

When applicable:

* I only have access to the `.length` property of an array`

This is the easiest one, loop through an array and find the position of a given array.

```java
int[] haystack = {1, 2, 3, 4, 5};
int needle = 3;
for (int i; i < haystack.length; i++) {
    if (haystack[i] == needle) {
        System.out.println("I found it!");
        return true;
    }
    System.out.println("I didn't find it :-(");
    return false;
}
```

## Sorting

### Bubble Sort

The simplest sort **O(N^2)**.

* Start in the 0th position and go to the end of the array
* If i+1 > i, swap positions
* If you reach the end and a swap occurred run again

```java
int[] haystack = {1, 3, 7, 4, 2};
boolean sorted = false;

while (!sorted) {
    for (int i = 0; i < haystack.length; i++;) {
        for (int j = 0; j < haystack.length - 1; j++;) {
            if (haystack[j] > haystack[j + 1]) {
                int tmp = haystack[j];
                haystack[j] = haystack[j + 1];
                haystack[j + 1] = tmp;
            }
        }
    }
}
```

### Quicksort

Divide and conquer.

Split input into N chunks, and run through those smaller subsets to solve things faster **O(LogN)** optimistically. Pessimistically, (reverse sorted array), it will be O(N^2).

Split an array at a Pivot point, and sort it so every element to the left is less than or equal to the pivot, and everything to the right is greater than the pivot. Then, select two more pivots, one to the left, and one to the right, and repeat until it's sorted.

```java
private void qs(int[] arr, int low, int high) {
    if (low => high) {
        return;
    }

    int privotIdx = partition(arr, low, high);
    qs(arr, low, pivotIdx - 1);
    qs(arr, pivotIdx + 1, high);
}

private int partition(int[] arr, int low, int high) {
    int pivot = arr[high];
    int idx = low - 1;

    for (int i = 0; i < high; i++) {
        if(arr[i] <= pivot) {
            idx++;
            int tmp = arr[i];
            arr[i] = arr[idx];
            arr[idx] = tmp;
        }
    }

    idx++;
    arr[high] = arr[idx];
    arr[idx] = pivot;

    return idx;
}

public void quicksort(int[] arr) {
    qs(arr, 0, arr.length - 1);
}
```

### Merge Sort

TODO

### Insertion Sort

TODO

## Binary Search

When applicable:

* Is it ordered?

Eliminate half of the total elements resulting in **O(LogN)**.

1. Start in the middle of the array
1. If x > array[i], move up
1. Else, move down
1. Continue until you find it

```java
public final int[] haystack = {1, 2, 3, 4, 5};

public boolean binarySearch(int needle) {
    int low = 0;
    int high = haystack.length;

    while (low < high) {
        mid = Math.floor(low + (high - low) / 2);
        value = haystack[m];

        if (value == needle) {
            return true;
        } else if (value > needle) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    return false;
}
```

## Linked Lists

There are two types of linked lists

Singly linked - A collection of nodes linked to the one behind them
```
A -> B -> C -> D
```

Doubly linked - The same thing, but you also get a link to the one ahead
```
A <-> B <-> C <-> D
```

Unlike arrays, deletion and insertion are possible, and they're pretty fast. Just remove the links from the previous and next nodes.

Prepend / append - O(1)
Deletion from end - O(1)
Get head / tail - O(1)
Insertion in middle - O(N)
Deletion in middle - O(N)

```java
public interface LinkedList<T> {
    public int getLength();
    public void insertAt(T item, int index);
    public T remove(T item);
    public T removeAt(int index);
    public void append(T item);
    public void prepend(T item);
    public T get(int index);
}
```

```java
public class Node<T> {
    public T value;
    public Node<T> prev;
    public Node<T> next;
    public Node<T>(T value) {
        this.value = value;
    }
}

public class DoublyLinkedList<T> {
    public int length;
    private Node<T> head;
    private Node<T> tail;

    public DoublyLinkedList() {
        this.length = 0;
        this.head = null;
        this.tail = null;
    }

    public void prepend(T item) {
        Node<T> node = Node(item);
        this.length++;
        if (this.head == null) {
            this.head = node;
            this.tail = node;
            return;
        }

        node.next = this.head;
        this.head.prev = node;
        this.head = node;
    }

    public void insertAt(T item, int index) {
        Node<T> node = Node(item);
        if(index > this.length) {
            throw Exception("oh no");
        } else if (index == this.length) {
            this.append(item);
            return;
        } else if (index == 0) {
            this.prepend(item);
            return;
        }
        Node<T> curr = this.head;
        for (int i = 0; curr != null && i < index; i++) {
            curr = curr.next;
        }

        Node<T> node = Node(item);
        node.next = curr;
        node.prev = curr.prev;
        curr.prev = node;

        if (curr.prev != null) {
            curr.prev.next = curr;
        }
        this.length++;
    }

    public void append(T item) {
        this.length++;
        Node<T> node = Node(item);
        if (this.tail == null) {
            this.head = node;
            this.tail = node;
            return;
        }

        node.prev = this.tail;
        this.tail.next = node;
        this.tail = node;
    }

    public Optional<T> remove(T item) {
        Node<T> curr = this.head;
        for(int i = 0; curr != null && i < this.length; i++) {
            if (curr.value == item) {
                break;
            }
            curr = curr.next;
        }
        if (curr == null) {
            return null;
        }

        if (this.length == 0) {
            this.head = null;
            this.tail = null;
            return null;
        }

        this.length--;
        if (curr.prev != null) {
            curr.prev = curr.next;
        }

        if (curr.next != null) {
            curr.next = curr.prev;
        }

        if (curr == this.head) {
            this.head = curr.next;
        }

        if (curr == this.tail) {
            this.tail = curr.prev;
        }

        curr.next = null;
        curr.prev = null;

        return curr.value;
    }

    public Optional<T> get(int index) {
        Node<T> curr = this.head;
        for (int i = 0; i < index && curr != null; i++) {
            curr = curr.next;
        }

        return Optional.ofNullable(curr.value);
    }

    public Optional<T> removeAt(int index) {
        ...
    }
}
```

### Array vs Linked List

* Arrays have access via index, linked list does not
* Arrays don't have a real "insert" without manually implementing for loops to shift over all values
* Arrays are allocated all up front

## Queue

Queues are FIFO (first in, first out) data structures. You can insert new elements to the end of the queue, and pop off from the front. These can be implemented using a singly linked list.

Pushing and popping from a queue are both constant time O(1). Typically you can also `peek`, which will look at the first element without popping.

```java
public class QNode<T>{
    public T value;
    public QNode<T> next;
    public QNode<T>(T value) {
        this.value = value;
    }
}

public class Queue<T> {
    public int length;
    private QNode<T> head;
    private QNode<T> tail;

    public Queue() {
        this.head = null;
        this.tail = null;
        this.length = 0;
    }

    public void enqueue(T item) {
        this.length++;
        QNode node = new QNode(item);

        if (this.tail == null) {
            this.head = node;
            this.tail = this.head;
            return;
        }

        this.tail.next = node;
        this.tail = node;
    }

    public Optional<T> dequeue() {
        if (this.head == null) {
            return null;
        }

        this.length--;
        QNode<T> h = this.head;
        this.head = this.head.next;

        h.next = null;

        return h.value;
    }

    public Optional<T> peek() {
        return Optional.ofNullable(this.head);
    }
}
```

## Stack

Stacks are LIFO (last in, first out), which let you push new elements onto the top, and pop elements off the top. Pushing and popping are again constant O(1).

```java
public class SNode<T> {
    public T value;
    public SNode<T> prev;

    public SNode<T>(T value) {
        this.value = value;
    }
}

public class Stack {
    public int length;
    private SNode<T> head;

    public Stack() {
        this.head = null;
        this.length = 0;
    }

    public void push(item: T) {
        this.length++;

        SNode<T> node = new SNode(item);
        if (this.head == null) {
            this.head = node;
            return;
        }

        node.prev = this.head;
        this.head = node;
    }

    public Optional<T> pop() {
        if (this.head == null) {
            return null;
        }

        this.length--;
        SNode<T> h = this.head;
        this.head = h.prev;
        h.prev = null;

        return h.value;
    }

    public Optional<T> peek() {
        return Optional.ofNullable(this.head);
    }
}
```

## Recursion

Whats always the problem with recursion? Recursion.

Recursion is something which calls itself over and over. The danger with recursion is stack overflows, to get around this use a stack instead.

```java
public int countToTen(int input) {
    if (input >= 10) {
        System.out.println("I'm done!");
        return input;
    }
    return countToTen(input++);
}
```

Recursion will be necessary for graph and tree traversal algorithms.
