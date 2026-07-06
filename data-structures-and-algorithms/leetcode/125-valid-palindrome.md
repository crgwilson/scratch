### Description
A phrase is a **palindrome** if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string `s`, return `true` _if it is a **palindrome**, or `false` otherwise._

### Examples
Example 1:
> Input: `s = "A man, a plan, a canal: Panama"`
> Output: `true`
> Explanation: `"amanaplanacanalpanama" is a palindrome.`

Example 2:
> Input: `s = "race a car"`
> Output: `false`
> Explanation: `"racecar" is not a palindrome.`

Example 3:
> Input: `s = " "`
> Output: `true`
> Explanation: `s is an empty string "" after removing non-alphanumeric chracters. Since an empty string reads the same forward and backward, it is a palindrome.`

### Solution
This is another problem using two pointers to maintain O(1) memory usage. The two pointers will start on either side of the string, and meet in the middle.
```python
class Solution:
	def alpha_numeric(self, c: str) -> bool:
		return (ord("A") <= ord(c) <= ord("Z") or
		ord("a") <= ord(c) <= ord("z") or
		ord("0") <= ord(c) <= ord("9"))
	
	def valid_palindrome(self, s: str) -> bool:
		l, r = 0, len(s) - 1	

		while l < r:
			while l < r and not self.alpha_numeric(s[l]):
				l += 1
			
			while r > l and not self.alpha_numeric(s[r]):
				r -= 1
				
			if s[l].lower() != s[r].lower():
				return False

			l, r = l + 1, r - 1
		
		return True
```