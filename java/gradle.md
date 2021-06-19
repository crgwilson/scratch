# Gradle

Gradle cheatsheet

## Gradle: Barebones build.gradle file

```groovy
plugins {
  id 'java'
}

repositories {
  mavenCentral()
}

jar {
  manifest {
    attributes 'Main-Class': 'somepackage'
  }
}

dependencies {
  testImplementation 'junit:junit:4.13.2'
}
```

## Gradle: Create a new Gradle project

```console
# gradle init
```

## Gradle: Install a specific Gradle wrapper

```console
# gradle wrapper --gradle-version=5.1.1
```

## Gradle: Stop Gradle daemon (via wrapper)

```console
# ./gradlew --stop
```
