### Description
Given an array of integers `nums` and an integer `target`, return _indices_ of the two numbers such that they add up to `target`.

You may assume that each input would have **exactly one solution**, and you may not use the same element twice.

You can return the answer in any order.

### Examples
Example 1:
> Input: `nums = [2, 7, 11, 15] target = 9`
> Output: `[0, 1]`
> Explanation: `Because nums[0] + nums[1] == 9, we return [0, 1]`

Example 2:
> Input: `nums = [3, 2, 4], target = 6`
> Output: `[1, 2]`

Example 3:
> Input: `nums = [3, 3] target = 6`
> Output: `[0, 1]`

### Solution
The brute force way to solve this problem is O(n^2), in which you use two nested for loops.
```python
class Solution:
	def two_sums(self, nums: list[int], target: int) -> list[int]:
		for i in range(len(nums)):
			for j in range(len(nums)):
				if i == j:
					continue
				
				if nums[i] + nums[j] == target:
					return [i, j]
```
...while this solution works, its time complexity sucks.

The generally accepted solution is O(n), using a hash map to keep track of indexes and values while iterating through the list a single time.
```python
class Solution:
	def two_sum(self, nums: list[int], target: int) -> list[int]:
		seen = {}
		for i in range(len(nums)):
			if target - nums[i] in seen:
				return [i, seen[target - nums[i]]]
			
			seen[nums[i]] = i
```