Divide and conquer [[Sorting-Algorithm]].

Split input into N chunks, and run through those smaller subsets to solve things faster **O(LogN)** optimistically. Pessimistically, (reverse sorted array), it will be O(N^2).

Split an array at a Pivot point, and sort it so every element to the left is less than or equal to the pivot, and everything to the right is greater than the pivot. Then, select two more pivots, one to the left, and one to the right, and repeat until it's sorted.

```java
private void qs(int[] arr, int low, int high) {
    if (low => high) {
        return;
    }

    int privotIdx = partition(arr, low, high);
    qs(arr, low, pivotIdx - 1);
    qs(arr, pivotIdx + 1, high);
}

private int partition(int[] arr, int low, int high) {
    int pivot = arr[high];
    int idx = low - 1;

    for (int i = 0; i < high; i++) {
        if(arr[i] <= pivot) {
            idx++;
            int tmp = arr[i];
            arr[i] = arr[idx];
            arr[idx] = tmp;
        }
    }

    idx++;
    arr[high] = arr[idx];
    arr[idx] = pivot;

    return idx;
}

public void quicksort(int[] arr) {
    qs(arr, 0, arr.length - 1);
}
```

## Sources:

* [[The Last Algorithms Course You'll Need]]