# Creational Patterns

## Abstract Factory

Abstract factories allow you to create families of related or dependent objects without specifying their concrete classes.

Use the Abstract Factory when:

* A system should be independent of how its products are created, composed, and represented.
* A system should be configured with one of multiple families of products.
* A family of related product objects is designed to be used together, and you need to enforce this constraint.
* You want to provide a class library of products, and you want to reveal just their interfaces, not their implementations.

An Abstract Factory will:

1. _Isolate concrete classes._ This pattern helps you control the classes of objects that an application creates. Clients manipulate instances through their abstract interfaces. Concrete factories, and concrete product classes (the thing the factory creates) are isolated in their implementation and do not appear in client code.
1. _Make exchanging product families easy._ The class of the concrete factory appears only once in the application, where it's instantiated. This makes it easy to change the concrete factory an application uses. It can use different product configurations simply by changing the concrete factory.
1. _It promotes consistency among products._ When product objects in a family are designed to work together, it's important that an application use objects from only one family at a time. Abstract Factories make this easy to enforce.
1. _Supporting new kinds of products is difficult._ Extending abstract factories to produce new kinds of products isn't easy as the interface of the Abstract Factory will be setup to accommodate the specifics of a certain product type.

Implementation Techniques:

1. _Factories are singletons._ An application typically only needs a single factory instance.
1. _Creating the products._ The Abstract Factory only provides the interface, it is up to concrete factories to handle the instantiation of concrete products.
1. _Defining extensible factories._ Having individual methods for each product type makes adding new products difficult, as you'd need to change the interface and all classes depending on it. Instead, consider adding an argument to your factory method acting as a signifier for the concrete product which it will be expected to produce.

Sample:

```java
public interface MazeFactory {
    public Maze makeMaze();
    public Wall makeWall();
    public Room makeRoom();
    public Door makeDoor();
}

public class EnchantedMazeFactory implements MazeFactory {
    public EnchantedMazeFactory() {}

    private Spell castSpell() {
        return new Spell();
    }

    public Room makeRoom(int n) {
        return new EnchantedRoom(n, castSpell());
    }

    public Door makeDoor(Room r1, Room r2) {
        return new DoorNeedingSpell(r1, r2);
    }
    // ...the rest of the interface...
}

public class BombedMazeFactory {
    public BombedMazeFactory() {}

    public wall MakeWall() {
        return new BombedWall();
    }

    public Room makeRoom(int n) {
        return new RoomWithABomb(n);
    }

    // ...the rest of the interface...
}

public class MazeGame {
    public Maze createMaze(MazeFactory factory) {
        Maze aMaze = factory.makeMaze(); 
        Room r1 = factory.makeMaze(1);
        Room r2 = factory.makeMaze(2);
        Door aDoor = factory.makeDoor(r1, r2);

        aMaze.addRoom(r1);
        aMaze.addRoom(r2);

        r1.setSide(North, factory.makeWall());
        r1.setSide(East, aDoor);
        r1.setSide(South, factory.makeWall());
        r1.setSide(West, factory.makeWall());

        r2.setSide(North, factory.makeWall());
        r2.setSide(East, factory.makeWall());
        r2.setSide(South, factory.makeWall());
        r2.setSide(West, aDoor);

        return aMaze;
    }
}

public class ClientApplication {
    public static void main(String[] args) {
        MazeGame game = new MazeGame();
        BombedMazeFactory factory = new BombedMazeFactory();

        Maze myMaze = game.createMaze(factory);
    }
}
```

Related Patterns:

1. Abstract Factories are often implemented using Factory Methods, but can also be implemented using Prototype.
1. A concrete factory is often a Singleton.

## Builder

Separate the construction of a complex object from its representation so that the same construction process can create different representations.

Use the Builder pattern when:

* The algorithm for creating a complex object should be independent of the parts that make up the object and how they're assembled.
* The construction process must allow different representations for the object that's constructed.

A Builder will:

1. _Let you vary a product's internal representation._ The Builder provides an abstract interface for constructing the product, hiding the internal structure of this process. This allows you to easily change the internal structure / construction process for that product.
1. _Isolate code for construction and representation._ The Builder pattern improves modularity by encapsulating the way a complex object is constructed and represented. Different clients can reuse the code from concrete builders which is only maintained in one place.
1. _Give you finer control over the construction process._ Unlike creation patterns that construct products in one shot, the Builder pattern constructs the product step by step under the director's control. Only when the product is finished does the director retrieve it from the builder. Giving you finer control over how the product is built.

Implementation Techniques:

1. _Assembly and construction interface._ Builders construct their products in step-by-step fashion. Therefore the interface must be general enough to allow the construction of products for all kinds of concrete builders.
1. _Why no abstract class for products?_ In the common case, the products produced by the concrete builders differ so greatly in their representation that there is little to gain from giving different products a common parent class.
1. _Empty methods as default in Builder._

Sample:

```java
public interface MazeBuilder {
    public void buildMaze();
    public void buildRoom(int room);
    public void buildDoor(int roomFrom, int roomTo);
    public Maze getMaze();
}

public class StandardMazeBuilder implements MazeBuilder {
    private Maze _currentMaze;

    public StandardMazeBuilder() {
        this._currentMaze = null;
    }

    public void buildMaze() {
        this._currentMaze = new Maze();
    }

    public void buildRoom(int n) {
        if (this._currentMaze.roomNo(n) == null) {
            Room room = new Room(n);
            this._currentMaze.addRoom(room);

            room.setSide(North, new Wall());
            room.setSide(South, new Wall());
            room.setSide(East, new Wall());
            room.setSide(West, new Wall());
        }
    }

    public void buildDoor(int n1, int n2) {
        Room r1 = this._currentMaze.RoomNo(n1);
        Room r2 = this._currentMaze.RoomNo(n2);
        Door d = new Door(r1, r2);

        r1.setSide(this.commonWall(r1, r2), d);
        r2.setSide(this.commonWall(r1, r2), d);
    }

    public Maze getMaze() {
        return this._currentMaze;
    }

    private Direction commonWall(Room r1, Room r2) {
        // Helper to find the direction of common walls between rooms
    }
}

public class MazeGame {
    public Maze createComplexMaze(MazeBuilder builder) {
        builder.buildRoom(1);
        builder.buildRoom(1001);
        return builder.getMaze();
    }
}

public class ClientApplication {
    public static void main(String[] args) {
        MazeGame game = new MazeGame();
        StandardMazeBuilder builder = new StandardMazeBuilder();

        game.createComplexMaze(builder);
        Maze myMaze = builder.getMaze();
    }
}
```

Related Patterns:

1. Abstract Factory is similar to Builder in that it too may construct complex objects. The primary difference is that the Builder pattern focuses on constructing a complex object step by step whereas an Abstract Factory's emphasis is on families of product objects being returned immediately.

## Factory Method

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

1. Abstract Factory is often implemented with factory methods.
1. Factory methods are usually called within Template Methods.
1. Prototypes don't require subclassing Creator. However, they often require an Initialize operation on the Product class. Creator uses Initialize to initialize the object. Factory Method doesn't require such an operation.

## Prototype

Use a Prototype when:
A Prototype will:
Implementation Techniques:
Sample:
Related Patterns:

## Singleton

Use a Singleton when:
A Singleton will:
Implementation Techniques:
Sample:
Related Patterns:
