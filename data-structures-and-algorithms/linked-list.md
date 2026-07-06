Linked lists are [[Data-Structure]]s which come in two flavors.

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

## Sources:

* [[The Last Algorithms Course You'll Need]]