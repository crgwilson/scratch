Merge sort is the best of [[Selection Sort]], [[Insertion Sort]], and [[Bubble Sort]]. It is a divide and conquer sorting algorithm.
![[Merge-Sort.png]]
1. Recursively sort 1st half of input array.
2. Repeat for 2nd half.
3. Merge two sorted sub lists into one.

For the merge step, you traverse both sorted arrays, taking the smallest item.
```python
# This is psuedo code

# C = output [length = n]
# A = 1st sorted array [n/2]
# B = 2nd sorted array [n/2]
# i = 0
# j = 0
for k = 0 to n-1:
	if A(i) < B(j):
		C(k) = A(i)
		i++
	elif (B(j) < A(i))
		C(k) = B(j)
		j++
```

#### Sources
* [[Algorithms Illuminated Omnibus Edition]]