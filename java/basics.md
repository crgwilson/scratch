# The Basics

Main methods are expected to have the signature
```java
public static void main(String[] args) {
    // do some cool stuff
}
```

Variables are declared with the data type in front of the symbol
```java
String myCoolString = "Wazzup Dawg";
```

## Method Header

```java
<AccessModifier> <Non-access Modifier> <Return type> <method name>() {
    // Do more stuff
}
```

## Access Modifiers

| Name | Description |
| ---- | ----------- |
| `public` | Any code from any class can use this method |
| `private` | Method can only be accessed within the same class |
| `protected` | Method can be accessed within the same package, or from within a child class |

If an access modifier is not provided, then by default the method will only be accessible within
the same package.

## Non-access Modifiers

| Name | Description |
| ---- | ----------- |
| `static` | Static can create methods which exist independently of any instance |
| `final` | A final variable can be explicitly initialized only once and can never be reassigned |
| `abstract` | Designates an abstract method to be implemented by child classes |
| `synchronized` | The method can only be access by one thread at a time |
| `volatile` | A thread accessing a volatile variable must merge its own private copy in with the master copy |

Non-access modifiers are optional

## Primitives

| Name | Default | Size | Type | Example |
| ---- | ------- | ---- | ---- | ------- |
| `byte` | 0 | 8-bit | Integral | `byte b = 100;` |
| `short` | 0 | 16-bit | Integral | `short s = 10000;` |
| `int` | 0 | 32-bit | Integral | `int i = 100000;` |
| `long` | 0L | 64-bit | Integral | `long l = 9999999;` |
| `float` | 0.0f | 32-bit | Floating point | `float f = 123.4f;` |
| `double` | 0.0d | 64-bit | Floating point | `double d = 12.4;` |
| `boolean` | FALSE | 1-bit | Boolean | `boolean b = true;` |
| `char` | `\u0000` | 16-bit | Character | `char c = 'C';` |

All primitives also have wrapper classes which provide some util methods

| Primitive Data Type | Wrapper Class |
| ------------------- | ------------- |
| `byte` | `Byte` |
| `short` | `Short` |
| `int` | `Integer` |
| `long` | `Long` |
| `float` | `Float` |
| `double` | `Double` |
| `boolean` | `Boolean` |
| `char` | `Character` |


## Type Inference

Local variables may have their type inferred using the `var` keyword
```java
public static void main(String[] args) {
    var isWaterWet = true;
}
```

## Overloading

You can overload methods by having the same method name with a different set of args, so long
as the method signature remains unique.

```java
public void echo(String mesage) {
    System.out.println(message);
}

public void echo(char message) {
    System.out.println(message);
}
```

## Records

Records are essentially immutable dataclasses. Fields are defined up front and getter and setter methods are
created magically, although you can add more methods to them if you want.
```java
public record Account(int id, int customerId, String type, double balance) {}
```

These are also referred to as POJOs (Plain ol Java Objects).

## Compilation and Running Something

`javac` is the command which can compile your java files into class files and `java` can run
the resulting class file.

```console
$ tree .
.
└── src
    └── example_package
            ├── ExampleJavaPackage.class
            └── ExampleJavaPackage.java

2 directories, 2 files
$ cd src
$ java example_package.ExampleJavaPackage
Wazzup Dawg
```
