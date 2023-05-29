# TestNG

TestNG is another unit testing framework for java which was inspired by JUnit, but has a few more features.
TestNG boasts:
* Parallel test execution
* Available integrations with tools such as selenium for integration tests
* The ability to group tests based on priority
* Data driven tests

## TestNG: Getting started

Just like every other test runtime in java, you'll need to install and configure it using your preferred build system. Here is
an example `build.gradle`.
```groovy
plugins {
  id 'java'
}

repositories {
  mavenCentral()
}

dependencies {
  testImplementation 'org.testng:testng:7.8.0'
}

test {
  useTestNG()
}
```

Test classes should follow [Apache's Standard Directory Layout](https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html).
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

Basic TestNG usage is pretty much exactly like that of JUnit. `@Test`, `@Before`, and `@After` annotations are all available within
`org.testng.annotations`, and the assertions are in `org.testng.Assert`. Here is a basic test.
```java
package com.helloworld;

import static org.testng.Assert.*;
import org.testng.annotations.Test;

public class testhelloworld {
  @test
  public void testhelloworld() {
    helloworld testobject = new helloworld();

    string got = testobject.sayhello();
    string expected = "hello world";

    assertequals(got, expected, "sayhello should say hello");
  }
}
```
