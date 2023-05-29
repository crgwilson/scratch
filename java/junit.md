# JUnit

JUnit is a unit testing framework for java.

## JUnit: Getting started

JUnit needs to be installed as a dependency and configured using your preferred build system. Here is an example `build.gradle`.
```groovy
plugins {
  id 'java'
}

repositories {
  mavenCentral()
}

dependencies {
  testImplementation 'junit:junit:4.13.2'
  // For JUnit 5 use the below lines
  // testImplementation 'org.junit.jupiter:junit-jupiter-api:5.8.1'
  // testRuntimeOnly 'org.junit.jupiter:junit-jupiter-api:5.8.1'
}

test {
  useJunit()
  // For JUnit 5 you'll want to call useJunitPlatform() instead
}
```

Your test classes need to be created alongside your java package in a `test` directory.
```console
src
├── main
│   └── java
│       └── com
│           └── helloworld
│               └── HelloWorld.java
└── test
    └── java
        └── com
            └── helloworld
                └── TestHelloWorld.java
```

Everything within the test src path will be picked up automagically and every method marked annotated as `@Test` will be executed.
In your tests you can use the assertion methods provided by `org.junit.Assert.*`. The usual suspects `assertEquals()`, `assertTrue()`, etc
are available.
```java
package com.helloworld;

import static org.junit.Assert.assertEquals;
import org.junit.Test;

public class TestHelloWorld {
  @Test
  public void testHelloWorld() {
    HelloWorld testObject = new HelloWorld();

    String got = testObject.sayHello();
    String expected = "Hello world";

    assertEquals("sayHello should say hello", expected, got);
  }
}
```

If you have certain setup and teardown operations you need to do for your unit tests you can use any of these annotations on another method.
* `@Before`
* `@BeforeClass`
* `@BeforeEach`
* `@BeforeAll`
* `@After`
* `@AfterClass`
* `@AfterEach`
* `@AfterAll`
