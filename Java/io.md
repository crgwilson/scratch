# I/O

Input / Output streams are used to read in and write out data to some IO (file, network socket, etc).

They're broken up into the interfaces:
* InputStream
* OutputStream

Common implementations include:
* FileInputStream
* ByteArrayInputStream
* FileOutputStream
* ByteArrayInputStream

InputStream and OutputStream work in bytes, Reader and Writer work in characters.

Reading stdin can be done with a scanner and system.
```java
// import java.util.Scanner;
Scanner scanner = new Scanner(System.in);

System.out.println("Gimmie your name brother: ");
String name = scanner.nextLine();

System.out.println("Gimmie your age brother: ");
int age = scanner.nextInt();
```

Reading files can be done with a BufferedReader
```java
// import java.io.BufferedReader;
// import java.io.FileReader;
try {
  BufferedReader reader = new BufferedReader(new FileReader("/tmp/my_cool_file.txt"));
  String firstLine = reader.readLine();  // This reads one line at a time
  System.out.println(firstLine);

  StringBuilder stringBuilder = new StringBuilder();
  reader.lines().forEach(line -> stringBuilder.append(line + " ")); // This reads every line in as a stream
  System.out.println("Rest of lines");
  System.out.println(stringBuilder);
} catch (IOException e) {
  e.printStackTrace();
}
```

In the above example we never closed our reader, which isn't ideal. Normally you can do this in a `finally` block
but you can also do a "try with resources" like below. This will automatically close the reader when we leave
the `try`.
```java
try(BufferedReader reader = new BufferedReader(new FileReader("/tmp/my_cool_file.txt"))) {
  // the rest of the original code
}
```

Both `java.io` and `java.nio` contain classes for working with files.
| `java.io` | `java.nio` |
| --------- | ---------- |
| Contains the `File` class | Contains the `Path`, `Paths`, and `Files` classes |
| Has some drawbacks | A better choice when writing new code |

The `Path` object represents a path to a file. The `Paths` class provides static methods to convert
strings to `Path` objects.

The `Files` class provides from helper methods for working with files.
```java
// import java.nio.Files;
// import java.nio.Path;
// import java.nio.Paths;
try {
  // This simple example creates a new, blank file
  Path path = Paths.get("/tmp/some_file.txt");
  if(Files.notExists(path)) {
    Files.createFile(path);
  }
} (IOException e) {
  e.printStackTrace();
}
```

There are similar methods available for working with directories as well.
```java
// import java.nio.Paths;
try {
  // Print out all files and directories in the current directory
  Files.list(Paths.get(".")).forEach(System.out::println);

  // Print out only files, not directories
  Files.list(Paths.get("."))
    .filter(file -> !Files.isDirectory(file))
    .forEach(System.out::println);

  if(File.notExists(Paths.get("/tmp/new_directory"))) {
    Files.createDirectory(Paths.get("/tmp/new_directory"));
  }
} catch (IOException e) {
  e.printStackTrace();
}
```

...and copying files
```java
Path pathToFile = Paths.get("some/file/path.txt");
Path pathToNewLocation = Paths.get("some/new/file/path.txt");

try {
  if(Files.notExists(pathToNewLocation) {
    Files.copy(pathToFile, pathToNewLocation);
  }
} catch (IOException e) {
  e.printStackTrace();
}
```
