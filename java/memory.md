# Memory Management

The JVM is responsible for managing all java memory, including allocations, deallocations
and GC.

When the JVM starts it reserves a small amount of memory (the heap) which is one of several
parts to all of java memory.
* Class area
* Heap
* Stack
* Program counter register
* Native method stack memory

## Stack vs Heap

| Stack | Heap |
| ----- | ---- |
| Only contains references and primitive values | Contains objects (which contain references and primitive values) |
| Accessed LIFO | Accessible whenever you have the address |
| Smaller and automatically deallocated | Bigger and deallocated by GC |
| Faster to access | Slower to access |
| Exists if the method is running | Exists for application lifetime |
| StackOverflowError when OOM | OutOfMemoryError when OOM |

```java
public class Example {
  public static void main(String[] args) {
    // stack memory
    int x = 5;
    double y = 3;
    boolean b = false;
    final int xy = 3;

    // stack and heap
    Person p = new Person();
    Address a = new Address();

    // heap memory
    a.setCity("Santa Clara");
    a.setCountry("United States");
    a.setNumber("123");
    a.sertStreetName("Java Street");
    a.setZipCode("456");

    p.setYearOfBirth(1993);
    p.setName("Craig");

    // connect address and person
    p.setAddress(a);  // Now the Person and Address objects are connected on the heap
  }
}
```

### Stack Memory

Stack memory is used for executing methods, it contains primitives and object references of
methods in the stack. The objects themselves are stored on the heap.

Stack memory allocates different blocks of memory for every method, and when the method has
finished, the block is removed.

The Stack:
| Method | Memory |
| ------ | ------ |
| **Method 3:** not calling any method | values and references of this method |
| **Method 2:** calling method 3 | values and references of this method |
| **Method 1:** calling method 2 | values and references of this method |

Within each stack frame, we have access to the elements within that frame (including both objects and references)
but nothing from any other frame.

### Heap Memory

Heap memory holds all objects that exist in the application. It is accessible from everywhere in the application
by way of the address of the object (the object reference). Objects on the heap contain primitive values and
references to other objects on the heap.

The Heap:
| Object | Memory |
| ------ | ------ |
| Object 1 | primitives and references |
| Object 2 | primitives and references |
| Object 3 | primitives and references |

Objects stored reference to other objects on the heap. When there are no more references from the stack to an
object within the heap, that object is considered to be "garbage" and will likely be cleaned up by the garbage
collector.

## Values vs References

### Primitives

Primitives live in the stack whereas wrapper classes (like `Integer`, `Boolean`, etc) live on the heap.
Accessing primitives on the stack is faster than objects, but objects are required when working with things
like collections.

```java
public class Example {
  public void method1() {
    int x = 0;
    method2(x);
  }

  public void method2(int x) {
    // Java passes primitives by value not by reference, so this mutation of 'x'
    // here will only occur within method2, and will not effect method1
    x = 2;
    int y = 1;
    method3();
  }

  public void method3() {
    int z = 2;
  }
}
```

### Objects

Objects live on the heap and are referenced via object references (ie: `Person@001`). When objects are passed
around, they are passed by reference, not by value. This means that mutating this object anywhere, will mutate it
globally (unlike primitives which are passed by value).

Using the `==` operator will always look at the object reference, meaning, two duplicate objects will not be seen as
equal. This is why `equals()` is a common method implemented by classes. These methods return `true` when the object
values are equal, even if the memory address is different.

### Final Variables

Final variables are immutable. Final primitive values work the same way you'd expect since primitives are passed around
by value, and therefore it is not possible to mutate the original.

However immutable objects can technically be mutable if not built correctly.

### Strings

Strings are unique in java since they're used so frequently. There is some extra plumbing to try and be extra efficient with
strings (since technically they are not primitives).

Java uses a string pool which means that when a string is exactly the same as a different one, it is assigned the same
reference. The string pool is a special place in memory for this purpose. So practically, if you create two strings, both `foo`,
java will only create one new string object, and hand our two references to it. You can force java to create a new object
by instantiating it like `String foo = new String("foo");`. Doing this will create the string outside of the string pool.

### Escaping References

Collections can hold multiple object references and is an object itself. When you return a collection, there are times where
you don't want to share the reference, given that would make your underlying objects mutable. In these cases you will want to
return a clone of your collection, to protect the original. Copying an object will create a shallow copy, which will leave the
underlying objects mutable. Ideally, in these cases you'll need a deep copy, cloning both the collection and the underlying objects.

For objects with a requirement for deep copies, refer to the `Cloneable` interface.

## Garbage Collection

Once an object no longer has a reference on the stack, it is considered eligible for garbage collection. Where `System.gc()` exists,
you cannot decide when GC happens, thats up to the JVM.

The garbage collector runs through all objects which exist in memory, and when a link to the stack is found, it is "marked" as a live object.
After live objects are marked, the remaining garbage needs to be deallocated, this happens in the 2nd stage called "sweeping". There are
a few different ways "sweeping" can be done which depends on your garbage collector.

Normal sweeping simply deallocates objects from memory. This method doesn't do any defragmentation of available heap making it
difficult to re-allocate the remaining space to objects of a certain size. Sweeping with compacting solves this problem by not
only de-allocating garbage, but also defragmenting the remaining objects in the memory region. There is also Sweeping with copying,
which is similar to sweeping with compacting, but the difference is remaining objects are copied over to a different region
of memory, and then the entire original region is deallocated.

### Types of Heap Memory

Memory is split into the Young Generation, the Old Generation, and the metaspace.

Young Generation is where all new objects are allocated. It is split up into the Eden space, and the Survivor space. During GC,
the young gen memory is cleaned up and if a certain object survives a certain number of GC cycles (configurable threshold) it is
promoted to the survivor space.

Old Generation is where objects which have survived many GC cycles are moved to from the survivor space. The process of moving from
the survivor space to old gen is called "scavenging", and the collectors doing this are called "scavengers". Old generation typically
requires a different GC strategy, since looking through this space is an expensive operation.

The metaspace is a permanent space in memory which contains:
* Klass structure
* Methods of classes
* Constants
* Annotations
* Optimizations

The metaspace is allocated when a class is loaded, and when classes are unloaded that bit of memory is released.

### Generational Garbage Collection

Marking objects is an expensive process and the application will need to be stopped in order to do this (stop the world pause).
GC is per generation, and works the best when most objects die young. Typically sweeping-with-copy is used. There are alternatives
to pausing the whole application which are dependent on your GC implementation.

#### Serial GC

* Young generation: mark and copy
* Old generation: mark sweep compact
* Runs on a single thread
* Stop-the-world implementation

#### Parallel GC

* Young generation: mark and copy
* Old generation: mark sweep compact
* Runs on multiple threads
* Stop-the-world implementation

#### CMS GC

* Young generation: mark and copy and stop the world
* Old generation: mark sweep compact and mostly concurrent (does not pause application)
* Runs on multiple threads
* Stop the world and mostly concurrent (with the running application)

#### G1GC

* Divides heap into small regions
* Keeps track of amount of live and dead objects
* Aims for shorted pauses possible
* Runs on multiple threads
* Concurrent and stop-the-world processes

#### ZGC

* Aims for 10ms pauses
* Uses "reference coloring" to mark objects
* Sweep and copy in parallel with application
* Running on multiple threads
* Fully concurrent

### Metrics for GC

The typical metrics to monitor specific to GC are:
* Allocation rate
* Heap population
* Mutation rate
* Object life span
* Mark time
* Compaction time
* GC cycle time

## JVM Tuning

To tune the JVM you need to gather metrics for how your application is running. For this, there is the `jstat` CLI using the
`-gcutil` flag. For a GUI you can also use VisualVM.

## Memory Leaks

Memory leaks are the accumulation of objects in memory that are no longer needed. Eventually they will fill up the available
heap, and the application will crash. Memory leaks will require applications to be restarted regularly as the longer they run
the slower they become, and eventually they OOM and crash.

```java
public class Example {
  public static void main(String[] args) {
    List<Person> list = new ArrayList<>();
    int i = 0;
    // This is an obvious example of a memory leak since we're never incrementing `i`
    // we will just add more Jeremy's into this list until the application crashes
    while(true) {
      Person p = new Person("Jeremy");
      list.add(p);
      if (i > 1000) {
        list = new ArrayList<>();
        i = 0;
      }
    }
  }
}
```

`java -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/myCoolHeapDump` is a handy JVM option to automatically take a heap dump on OOM.

Common solutions for memory leaks include:
* Set the object to null in certain specific situations
* Close resources such as streams and connections
* Avoid string concats; use string builder instead
* Be careful with static collections holding objects
* Overwrite `hashCode` and `equals` (especially when custom objects are added to hash sets)
