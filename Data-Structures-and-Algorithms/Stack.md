Stacks are LIFO (last in, first out), [[Data-Structure]]s which let you push new elements onto the top, and pop elements off the top. Pushing and popping are again constant O(1).

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

## Sources:

* [[The Last Algorithms Course You'll Need]]