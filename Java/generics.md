# Generics

Generics let you write a method which can accept any type of object eliminating the need for
excessive casting and reflection.

Basic example:
```java
import java.util.Arrays;
import java.util.List;

public class Example {
  public static void main(String[] args) {
    String[] words = {"foo", "bar", "baz"};
    Integer[] numbers = {1, 2, 3};

    List<String> wordsList = convertArrayToList(words);
    List<Integer> numbersList = convertArrayToList(numbers);
  }

  // This method accepts an array of any type
  // so it works with both 'words' and 'numbers'
  private static <T> List<T> convertArrayToList(T[] array) {
    return Arrays.asList(array);
  }
}
```

There are cases where you need generics, but you also want some amount of restriction. For example
a method which can only accept types of numbers, instead of any object. In these cases you can use
a "bounded generic".

```java
// This method will only accept objects that implement the `Numver` interface
private static <T extends Number> List<T> convertArrayToList(T[] array) {
    return Arrays.asList(array);
}
```

When using collections you would expect that you'd be able to pass in a `List<SomeChildType>` into a method
expecting `List<SomeParentType>`, however this doesn't actually work even though `SomeChildType` is a subclass
of `SomeParentType`. In cases like this wildcard generics can be used.
```java
// This method will accept a list of ClothingItems, and all sub-types of
// ClothingItem (ShirtItem, JacketItem, ShoeItem, whatever)
static void checkoutAllItems(List<? extends ClothingItem> clothingItems) {
  // do some stuff
}
```
