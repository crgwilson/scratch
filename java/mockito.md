# Mockito

[Mockito](site.mockito.org) is the most popular Java mocking framework

## Mockito: Getting started

To install Mockito you will need to declare a dependency on `mockito-core` using your favorite build system.
Here is an example `build.gradle`.
```groovy
plugins {
  id 'java'
}

repositories {
  mavenCentral()
}

dependencies {
  testImplementation 'org.mockito:mockito-core:3.+'
}
```

Now you can mock classes in your tests...
```java
import static org.mockito.Mockito.*;

List mockedList = mock(List.class);
mockedList.add("foo");
mockedList.clear();

// Test to see that the appropriate methods were actually called
verify(mockedList).add("foo");
verify(mockedList).clear();
```

...and stub method calls...
```java
LinkedList mockedList = mock(LinkedList.class);
when(mockedList.get(69)).thenReturn("nice");

// This will print out "nice"
System.out.println(mockedList.get(69));

// This will return null because we didn't stub with 0 as an input
System.out.println(mockedList.get(0));
```

...and create spies...
```java
List<String> list = new ArrayList<String>();
// Wrap our list in a spy
List<String> spyList = spy(list);

spyList.add("foo");
spyList.add("bar");

verify(spyList).add("foo");
verify(spyList).add("bar");

assertThat(spyList).hasSize(2);
```

...but whats the difference between a mock and a spy? Well you can probably figure it out from the above examples. A mock
is a bare-bones class with pretty much no functionality at all, whereas a spy is a wrapper atop a class. When spies
are used, the underlying class is still called so in some cases it may be necessary to stub certain methods of the spy.
```java
List<String> list = new ArrayList<String>();
List<String> spyList = spy(list);

assertEquals(0, spyList.size());

doReturn(100).when(spyList).size();
assertThat(spyList).hasSize(100);
```

One important thing to remember is that `doReturn()` and `when()` expect their inputs to be a mock. If you pass in a "real"
object instead, you'll be greeted with a `NotAMockException`.
