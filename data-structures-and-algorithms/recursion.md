What's always the problem with recursion? Recursion.

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

## Sources:

* [[The Last Algorithms Course You'll Need]]