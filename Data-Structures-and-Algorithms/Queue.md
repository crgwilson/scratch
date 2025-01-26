Queues are FIFO (first in, first out) [[Data-Structure]]s. You can insert new elements to the end of the queue, and pop off from the front. These can be implemented using a singly linked list.

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

## Sources:

* [[The Last Algorithms Course You'll Need]]