## Big O Time Complexity

Big O categorizes your algorithm's time or memory requirements based on input. It is not meant to be an exact measurement. As your input grows how fast does your computation or memory grow?

For a stupid example, this code...
```typescript
function sum_char_codes(n: string): number {
    let sum = 0;
    for (let i = 0; i < n.length; ++i) {
        sum += n.charCodeAt(i);
    }
    return sum;
}
```
...is **O(N)** as it grows linearly. If the length of input string `n`, increases in length by 50%, our function will take roughly 50% longer since we're looping through it.

Time Complexities

* O(1) constant no matter the input
* O(LogN) binary search trees
* O(N)
* O(NLogN) quicksort
* O(N^2) nested for loop
* O(2^N)
* O(N!)

The logarithm of a number if the number of steps down to 1 in binary, IE log 4096 = 12
```
Start   - 4096
Step 1  - 2048
Step 2  - 1024
Step 3  - 512
Step 4  - 256
Step 5  - 128
Step 6  - 64
Step 7  - 32
Step 8  - 16
Step 9  - 8
Step 10 - 4
Step 11 - 2
Step 12 - 1
```

### Important Concepts

* Look for loops
* Always drop constants IE: O(2N) == O(N)
* Always assume worst case
* If you half at each step, it's likely O(LogN) or O(NLogN)

## Sources

* [[The Last Algorithms Course You'll Need]]