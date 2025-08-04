The Prototype is one of the [[Creational-Patterns]] described in [[Design Patterns Elements of Reusable Object-Oriented Software]].

Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this Prototype.

Use a Prototype when:

* The classes to instantiate are specified at run-time, for example, by dynamic loading
* To avoid building a class hierarchy of factories that parallels the class hierarchy of products
* Instances of a class can have one of only a few different combinations of state. It may be more convenient to install a corresponding number of prototypes and clone them rather than instantiating the class manually, each time with the appropriate state.

A Prototype will:

Implementation Techniques:

Sample:

Related Patterns: