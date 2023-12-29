# Algorithms

# Basics

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
...is O(N) as it grows linearly. If the length of input string `n`, increases in length by 50%, our function will take roughly 50% longer since we're looping through it.

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

* Retrieving a value knowing the index is O(1)
* Retrieving a value not knowing the index is O(N)

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

## Binary Search

When applicable:

* Is it ordered?

Eliminate half of the total elements resulting in O(LogN)

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

## Bubble Sort

The simplest sort O(N^2).

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

        if (Objects.isNull(this.tail)) {
            this.head = node;
            this.tail = this.head;
            return;
        }

        this.tail.next = node;
        this.tail = node;
    }

    public Optional<T> dequeue() {
        if (Objects.isNull(this.head)) {
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
        if (Objects.isNull(this.head)) {
            this.head = node;
            return;
        }

        node.prev = this.head;
        this.head = node;
    }

    public Optional<T> pop() {
        if (Objects.isNull(this.head)) {
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
