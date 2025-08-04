# Concurrency

Java has the `Thread` class which you can use to write multi-threaded applications.
```java
public class ThreadExample extends Thread {
  public void run() {
    System.out.println("howdy from " = this.getName);
  }
}
```

```java
public class Example {
  public static void main(String[] args) {
    Thread threadOne = new ThreadExample();
    Thread threadTwo = new ThreadExample();
    Thread threadThree = new Thread(() -> System.out.println("Howdy from a lambda style runnable"));

    threadOne.setName("numbah one");
    threadTwo.setName("numbah two");

    threadOne.start();
    threadTwo.start();
  }
}
```

The Thread class implements the `Runnable` interface which expects a single method `run()`.
Runnables can be passed into the ExecutorService class.
```java
ExecutorService executorService = Executors.newFixedThreadPool(2);  // num of threads in pool
executorService.submit(new _05_04.before.SomeRunnable());
executorService.submit(() -> System.out.println("Howdy from an executor service runnable"));

executorService.shutdown();
```

To keep multiple threads from running the same block of code at the same time you can use "Synchronized methods".
```java
public synchronized void oneAtATime() {
  System.out.println("Only one thread can do this at a time");
}
```
