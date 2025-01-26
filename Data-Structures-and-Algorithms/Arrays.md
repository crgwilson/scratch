An array is a [[Data-Structure]] contiguous memory space which contains a certain amount of bytes.

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

## Searching Algorithms
### Linear Search

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

### Binary Search

When applicable:

* Is it ordered?

Eliminate half of the total elements resulting in **O(LogN)**.

1. Start in the middle of the array
1. If `x > array[i]`, move up
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

## Sorting

You can use common sorting algorithms to sort arrays:

* [[Bubble-Sort]]
* [[Quick-Sort]]
* [[Insertion-Sort]]
* [[Selection-Sort]]
* [[Merge-Sort]]

## Sources

* [[The Last Algorithms Course You'll Need]]