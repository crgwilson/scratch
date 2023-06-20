# Functional Programming in Java

## Functional Interfaces

Functional interfaces are interfaces with a single method
```java
@FunctionalInterface
public interface Example {
  void sayHowdyPartner();
}
```

## Lambdas

Lambdas can be used with anonymous methods to implement functional interfaces without as much
boilerplate.
```java
Example sayHowdyPartner = () -> System.out.println("hoooowdy partner");
```

Lambdas can also be used for method references
```java
List<Integer> numbers = Arrays.asList(1, 2, 3);
// Run NumberUtils.evenOrOdd() on every number in numbers
numbers.forEach(NumberUtils::evenOrOdd(number));
```

## Streams

Streams offer you another way to express some logic onto a collection of elements. "Intermediate" operations
return another stream, and can be chained together, and "terminal" operations go at the end to execute
your logic.

```java
// In this example `sorted()` is the intermediate operation and
// `forEach` is terminal.
List<Integer> numbers = Arrays.asList(1, 2, 3);
numbers.stream().sorted()
  .forEach(System.out::println);
```
