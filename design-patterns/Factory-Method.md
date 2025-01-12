The Factory Method is one of the [[Creational-Patterns]] described in [[Design Patterns Elements of Reusable Object-Oriented Software]].

Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses.

Use a Factory Method when:

* A class can't anticipate the class of objects it must create.
* A class wants its subclasses to specify the objects it creates.
* Classes delegate responsibility to one of several helper subclasses, and you want to localize the knowledge of which helper subclass is the delegate.

A Factory Method will:

1. _Provides hooks for subclasses._ Creating objects inside a class with a factory method is always more flexible than creating an object directly. Having a Factory Method also gives subclasses a hook for providing an extended version of an object.
1. _Connects parallel class hierarchies._

Implementation Techniques:

1. _Two major varieties._ The two main variations of the Factory Method pattern are the Creator class as an abstract class, and does not provide an implementation for the factory method it declares, and the case when the Creator is a concrete class and provides a default implementation for the factory method.
1. _Parametrized factory methods._ Another variation on the pattern lets the factory method create _multiple_ kinds of products. The factory method takes a parameter that identifies the kind of object to create (See below).
1. _Language-specific varients and issues._ Different languages lend themselves to other interesting variations and caveats.
1. _Using templates to avoid subclasses._
1. _Naming conventions._ It's good practice to use naming conventions that make it clear you're using factory methods. For example `public MyClass doMakeMyClass()`.

```java
public Product create(ProductId id) {
    if (id == YOURS) {
        return new YourProduct();
    }
    if (id == MINE) {
        return new MyProduct();
    }
    if (id == THEIRS) {
        return new TheirProduct();
    }
}
```

Sample:

```java
public interface MazeGame {
    public Maze makeMaze();
    public Room makeRoom(int n);
    public Wall makeWall();
    public Door makeDoor(Room r1, Room r2);
}

// This one is super straight forward, so I won't be writing out the sample implementation.
```

Related Patterns:

1. [[Abstract-Factory]] is often implemented with factory methods.
1. Factory methods are usually called within [[Template-Method]]s.
1. [[Prototype]]s don't require subclassing Creator. However, they often require an Initialize operation on the Product class. Creator uses Initialize to initialize the object. [[Factory-Method]] doesn't require such an operation.