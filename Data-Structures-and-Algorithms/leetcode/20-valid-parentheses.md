### Description
Given a string `s` containing just the characters `(`, `)`, `{`, `}`, `[`, `]`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

### Examples
Example 1:
> Input: `s = "()"`
> Output: `true`

Example 2:
> Input: `s = "()[]{}"`
> Output: `true`

Example 3:
> Input: `s = "(]"`
> Output: `false`

Example 4:
> Input: `s = "([])"`
> Output: `true`

### Solution
Given we care about the ordering of the brackets, and each is meant to come in a pair, a stack is a natural fit for this. A stack would give us a solution which is both O(n) in time complexity and O(n) in memory usage.
```python3
class Solution:
	def is_valid(self, s: str) -> bool:
		stack = []
		close_to_open = {
			")": "(",
			"]": "[",
			"}": "{",
		}
		
		for c in s:
			if c in close_to_open:
				if stack and stack[-1] == close_to_open[c]:
					stack.pop()
				else:
					return False
			else:
				stack.append(c)
		
		if stack:
			return False
		
		return True
```