The simplest [[Sorting-Algorithm]], which sorts at **O(N^2)**.

* Start in the 0th position and go to the end of the array
* If i+1 > i, swap positions
* If you reach the end and a swap occurred run again

![](../Excalidraw/Bubble-sort.png)

```java
int[] haystack = {1, 3, 7, 4, 2};
boolean sorted = false;

while (!sorted) {
    for (int i = 0; i < haystack.length; i++;) {
        for (int j = 0; j < haystack.length - 1; j++;) {
            if (haystack[j] > haystack[j + 1]) {
                int tmp = haystack[j];
                haystack[j] = haystack[j + 1];
                haystack[j + 1] = tmp;
            }
        }
    }
}
```

## Sources:

* [[The Last Algorithms Course You'll Need]]