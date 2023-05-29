# Gradle

Gradle is a build framework most commonly used for Java projects which can be configured using either a Groovy or Kotlin DSL

It's big and complicated.

## Gradle: Getting started

A new gradle project can be initialized with `gradle init`. It will create a few files in your cwd needed to build a new project.
This can be done with your system gradle, but in all cases you'll want to also create your gradle wrapper. The gradle wrapper script
can let you use different versions of gradle without having to manually install different packages everywhere.

`gradle wrapper --gradle-version 7.6`

From there, you can use your local environment's gradle by calling `gradlew <task name>`
```
├── build.gradle
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
└── settings.gradle
```

### Gradle: `build.gradle`

This file is the equivalent to your `Makefile` or `Rakefile`. It is where your plugins can be included, tasks defined, and any other
necessary logic.

Everything within the `build.gradle` file references methods from one of gradle's [classes](https://docs.gradle.org/current/javadoc/org/gradle/api/Project.html) (Task, Dependencies, Plugins, etc).

Each plugin you import simply adds "tasks" to be used when building, testing, packaging your project.
```groovy
plugins {
    id 'java'
}
```

You define your dependencies in here too, in this case pulling dependencies from the `mavenCentral()` repository.
```groovy
repositories {
    mavenCentral()
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}

test {
    useJUnitPlatform()
}
```

There is also some configuration which can be set within your build file, in this example we're telling gradle where our
main class is.
```groovy
plugins {
  id 'java'
}

repositories {
  mavenCentral()
}

jar {
  manifest {
    attributes 'Main-Class': 'com.somepackage.helloWorld'
  }
}
```

### Gradle: `settings.gradle`

The `settings.gradle` file is used for multi-project repos. When multiple directories are contained within the scope of one project
they can be included with `include 'myProjectName'`.

In this example gradle will look for a `myProjectName` directory.

### Gradle: `gradlew` / `gradlew.bat`

The gradle wrapper (or gradlew) script wraps the gradle CLI and keeps you from needing to install N number of gradle versions locally.
Based on the required versions given in your `build.gradle` file, the gradlew will automatically install that, and delegate all of your
commands to the correct bin.

## Gradle: Install a specific Gradle wrapper

```console
gradle wrapper --gradle-version=5.1.1
```

## Gradle: Stop Gradle daemon (via wrapper)

```console
./gradlew --stop
```
