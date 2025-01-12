The Builder is one of the [[Creational-Patterns]] described in [[Design Patterns Elements of Reusable Object-Oriented Software]].

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

1. [[Abstract-Factory]] is similar to Builder in that it too may construct complex objects. The primary difference is that the Builder pattern focuses on constructing a complex object step by step whereas an [[Abstract-Factory]]'s emphasis is on families of product objects being returned immediately.