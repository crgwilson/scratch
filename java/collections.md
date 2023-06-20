# Collections

Notes regarding the interfaces and classes available with java collections.

All java collections are available in `java.util.*`. Collections can be instantiated just
like any other type.

For example:
```java
import java.util.ArrayList;
import java.util.Collection;

public class Example {
  public static void main(String[] args) {
    // When instantiating collections be sure to use the most abstract one you can
    // like List, or even Collection
    Collection<String> c = new ArrayList<>();
    c.add("Howdy");
    c.add("partner");
  }
}
```

## Interfaces

Java Collections relies on these interfaces for all its various implementations:
* Collection
* Map
* List
* Queue
* Deque
* Set

Some common implementations for these interfaces include:
* HashMap
* LinkedHashMap
* ArrayList
* Vector
* Stack
* LinkedList
* ArrayDeque
* PriorityQueue
* TreeSet
* HashSet
* LinkedHashSet

The naming for these objects tell you both the sort of algorithm used in its implementation, and what
interface it is implementing
`<Implementation Style><Interface>`

ie: HashMap

### Collection Interface

The `Collection` interface is the parent of all other interfaces within collections, providing common methods which
will be seen all throughout the library. Methods with asterisks are optional.

| Insert Elements | Remove Elements | Iterate Collection | Inspect Collection | Misc |
| --------------- | --------------- | ------------------ | ------------------ | ---- |
| `boolean add(E e)*` | `void clear()*` | `void forEach(Consumer<T> a)` | `boolean contains(Object o)` | `boolean equals(Object o)` |
| `boolean addAll(Collection<? extends E> e)*` | `boolean remove(Object o)*` | `Iterator<E> iterator()` | `boolean containsAll(Collection<?> c)` | `int hashCode()` |
| - | `boolean removeAll(Collection<?> c)*` | `Stream<E> parallelStream()` | `boolean isEmpty()` | `Object[] toArray()` |
| - | `boolean removeIf(Predicate<? super E> f)` | `Spliterator<E> spliterator()` | `int size()` | `T[] toArray(IntFunction<T[]> g)` |
| - | `boolean retainAll(Collection<?> c)*` | `Stream<E> stream()` | - | `T[] toArray(T [])` |


## Iterating

Collections can be iterated upon be either using loops, iterables, or streams.

Loops are a standard programming construct, in order to loop over a collection that collection must implement the `Iterable` interface.
Iterables require the same interface to be implemented and provide an iterator capable of forward traversal.
Streams probide a sequence of elements from a source collection that can have one or more operations (lambda expressions and the like).

Iterator example:
```java
public class Example {
  public static void main(String[] args) {
    Collection<String> c = new ArrayList<>(Arrays.asList("foo", "bar", "baz"));

    Iterator<String> iterator = c.iterator();
    System.out.println(iterator.next());  // Prints foo
    System.out.println(iterator.next());  // Prints bar
    System.out.println(iterator.next());  // Prints baz

    // ...or with a while loop...
    while (iterator.hasNext()) {
      String str = iterator.next();
      System.out.println(str);
    }

    // ...or with a for each loop..
    for (String str : c) {
      System.out.println(str);
    }
  }
}
```

Stream example:
```java
public class Example {
  public static void main(String[] args) {
    Collection<String> c = new ArrayList<>(Arrays.asList("foo", "bar", "baz"));

    // This whole mess tests if the string is "foo", and if so, prints it out
    c.stream()
      .filter(new Predicate<String>() {
        @Override
        public boolean test(String s) {
          return str.equals("foo");
        }
      }).forEach(new Consumer<String>() {
        @Override
        public void accept(String s) {
          System.out.println(s);
        }
      });

    // ...or with a stream and a lambda expression...
    c.stream()
      .filter(str -> str.equals("foo"))
      .forEach(str -> System.out.println(str));
  }
}
```

Note: You cannot modify a collection while iterating. If you need to add or remove elements while in a loop, you'll need to duplicate the
collection.

## Set

Sets are like lists which do not allow duplicate elements

`HashSet` and `LinkedHashSet` implement `Set`, `HashSet` is unordered, `LinkedHashSet` uses a linked list, and is therefore ordered.

There is also the `TreeSet` which uses a binary search tree to organize its elements, and implements the `NavigableSet` interface.

## List

Lists are an ordered collection that provide positional insertion, removal, etc and are likely the most commonly used collection.
The `List` interface is implemented by:
* `ArrayList`
* `LinkedList` (this one also implements `Deque` which is a queue)
* `Vector`
* `Stack`

Note that both `Vector` and `Stack` pre-date collections, and are considered to be obsolete.

`ArrayList` is backed by an array, but is able to change its size automatically as you outgrow the initial size.

Generally `LinkedList`s are good for adding elements, but bad for traversal.

```java
// import java.util.LinkedList;
LinkedList<String> llist = new LinkedList<>();
llist.add("foo");
llist.add("bar");
llist.add("baz");
```

## Queue

The queue is your FIFO collection. Interfaces are:
* `Queue`
* `Deque`

Implementations are:
* `LinkedList`
* `ArrayDeque`
* `PriorityQueue`

`Deque` is a double-ended queue, and let's you do operations on either end of the queue, whereas other implementations
only let you add to the back and pull from the front.

`PriorityQueue` let's you provide a comparator which will be used to determine which elements should be pulled from the
queue first.

## Map

Map is your dictionary equivalent most commonly used as a `HashMap`. `Map` is the only collection interface which does
not inherit from the `Collection` interface.

Keys must implement `hashCode` and `equals` methods.

Interfaces are:
* `Map`
* `SortedMap`
* `NavigableMap`

Implementations are:
* `HashMap`
* `LinkedHashMap`
* `TreeMap`

```java
// import java.util.HashMap;
HashMap<String, Integer> basket = new HashMap<>();
basket.put("apple", 1);
System.out.println(basket.get("apple"));
```
