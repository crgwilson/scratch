The Prototype is one of the [[Creational-Patterns]] described in [[Design Patterns Elements of Reusable Object-Oriented Software]].

Ensure a class only has one instance, and provide a global point of access to it.

Use a Singleton when:

* There must be exactly one instance of a class, and it must be accessible to clients from a well-known access point.
* The sole instance should be extensible by subclassing, and clients should be able to use an extended instance without modifying their code.

A Singleton will:

1. _Controlled access to sole instance._ Because the Singleton class encapsulates its sole instance, it can have strict control over how and when clients access it.
1. _Reduced name space._ The Singleton pattern is an improvement over global variables. It avoids polluting the name space with global variables that store sole instances.
1. _Permits refinement of operations and representations._ The Singleton class may be subclassed, and it's easy to configure an application with an instance of this extended class. You can configure the application with an instance of the class you need at run-time.
1. _Permits a variable number of instances._ The pattern makes it easy to change your mind and allow more than one instance of the Singleton class. Moreover, you can use the same approach to control the number of instances that the application uses. Only the operation that grants access to the Singleton instance needs to change.
1. _More flexible than class operations._ Another way to package a singleton's functionality is to use class operations (that is, static methods). But both of these language techniqures make it hard to change a design to allow more than one instance of a class. Moreover, static methods can be overridden polymorphically by subclasses.

Implementation Techniques:

1. _Ensuring a unique instance._ The Singleton pattern makes the sole instance a normal instance of a class, but that class is written so that only one instance can ever be created.
1. _Subclassing the Singleton class._ Determine which Singleton you want to use in your `instance()` method, and install that one specifically.

Sample:

```java
public interface MazeFactory {
    public static MazeFactory instance();
}

public class MazeFactorySingleton implements MazeFactory {
    private MazeFactorySingleton _instance;

    public MazeFactorySingleton() {
        this._instance = null;
    }

    public static MazeFactorySingleton() {
        if (this._instance == null) {
            this._instance = new MazeFactorySingleton();
        }
        return this._instance;
    }
}
```

Related Patterns:

1. Many patterns can be implemented using the Singleton pattern. See Abstract Factory, Builder, and Prototype.