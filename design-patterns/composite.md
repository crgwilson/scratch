The Composite is one of the [[Creational-Patterns]] described in [[Design Patterns Elements of Reusable Object-Oriented Software]].

Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly.

![[../Excalidraw/Composite.png]]

Use a Composite when:

* You want to represent part-whole hierarchies of objects.
* You want clients to be able to ignore the difference between compositions of objects and individual objects. Clients will treat all objects in the composite structure uniformly.

A Composite will:

1. Defines class hierarchies consisting of primitive objects and composite objects. Primitive objects can be composed into more complex objects which in turn can be composed, and so on recursively. Wherever client code expects a primitive object, it can also take a composite object.
2. Makes the client simple. Clients can treat composite structures and individual objects uniformly. Clients normally don't know (and shouldn't care) whether they're dealing with a leaf or a composite component. This simplified client code, because it avoids having to write tag-and-case-statement-style functions over the classes that define the composition.
3. Makes it easier to add new kinds of components. Newly defined composite or leaf subclasses work automatically with existing structures and client code. Clients don't have to be changed for new component classes.
4. Can make your design overly general. The disadvantage of making it easy to add new components is that it makes it harder to restrict the components of a composite. Sometimes you want a composite to have only certain components. With composite, you can't rely on the type system to enforce those constraints for you. You'll have to use run-time checks instead.

Implementation Techniques:

1. _Explicit parent references._ Maintaining references from child components to their parent can simplify the traversal and management of a composite structure. The parent reference simplifies moving up the structure and deleting the component.
1. _Sharing components._ It's often useful to share components, for example, to reduce storage requirements. But when a component can have no more than one parent, sharing components becomes difficult. A possible solution is for children to store multiple parents. But that can lead to ambiguities as a request propagates up the structure. The [[Flyweight]] pattern shows how to rework a design to avoid storing parents altogether. It works in cases where children can avoid sending parent requests by _externalizing_ some or all of their state.
1. _Maximizing the component interface._ One of the goals of the composite pattern is to make clients unaware of the specific leaf or composite classes they're using. To attain this goal, the component class should define as common operations for composite and leaf classes as possible. The component class usually provides default implementations for these operations, and leaf and composite subclasses will override them.
1. _Declaring the child management operations._ Although the composite class implements the Add and Remove operations for managing children, an important issue in the composite pattern is which classes declare these operations in the composite class hierarchy. Should we declare these operations in the component and make them meaningful for leaf classes, or should we declare and define them only in the composite subclasses?
1. _Should component implement a list of components?_ You might be tempted to define the set of children as an instance variable in the component class where the child access and management operations are declared. But putting the child pointer in the base class incurs a space penalty for every leaf, even though a leaf never has children. This is worthwhile only if there are relatively few children in the structure.
1. _Child ordering._ Many designs specify an ordering on the children of composite. If composites represent parse trees, then compound statements can be instances of a composite whose children must be ordered to reflect the program. When child ordering is an issue, you must design child access and management interfaces carefully to manage the sequence of children. The [[Iterator]] pattern can guide you in this.
1. _Caching to improve performance._ If you need to traverse or search compositions frequently, the composite class can cache traversal or search information about its children. The composite can cache actual results or just information that lets it short-circuit the traversal or search. Changes to a component will require invalidating the caches of its parents. This works best when components know their parents. So if you're using caching, you need to define an interface for telling composites that their caches are invalid.
1. _Who should delete components?_ In languages without garbage collection, it's usually best to make a composite responsible for deleting its children when it's destroyed. An exception to this rule is when leaf objects are immutable and thus can be shared.
1. _What's the best data structure for storing components?_ Composites may use a variety of data structures to store their children, including linked lists, trees, arrays, and hash tables. The choice of data structure depends on efficiency. In fact, it isn't even necessary to use general-purpose data structures at all. Sometimes composites have a variable for each child, although this requires each subclass of composite to implement its own management interface. See [[Interpreter]] for an example.

Sample:

TODO

Related Patterns:

1. Often the component-parent link is used for [[Chain-of-Responsibility]].
2. [[Decorator]] is often used with composite. When decorators and composites are used together, they will usually have a common parent class. So decorators will have to support the component interface with operations like Add, Remove, and GetChild.
3. [[Flyweight]] lets you share components, but they can no longer refer to their parents.
4. [[Iterator]] can be used to traverse composites.
5. [[Visitor]] localizes operations and behavior that would otherwise be distributed across composite and leaf classes.