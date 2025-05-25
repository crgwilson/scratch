### Description
You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists into one **sorted** list. The list should be made by splicing together the nodes of the first two lists.

_Return the head of the merged linked list._

### Examples
```
1->2->4
1->3->4

--------

1->1->2->3->4->4
```

Example 1:
> Input: `list1 = [1, 2, 4], list2 = [1, 3, 4]`
> Output: `[1, 1, 2, 3, 4, 4]`

Example 2:
> Input: `list1 = [], list2 = []`
> Output: `[]`

Example 3:
> Input: `list1 = [], list2 = [0]`
> Output: `[0]`
### Solution
This one is a simple linked list problem. Given both lists are already sorted we just need to talk through them both and append the smaller of the two items to our return list. For cases where the size of both lists differ, we can just append the remainder of the non-empty list to the end.
```python
class Solution:
	def merge_two_sorted_lists(list1: Node, list2: Node) -> Node:
		dummy = Node()
		tail = dummy

		while list1 and list2:
			if list1.val < list2.val:
				tail.next = list1
				list1 = list1.next
			else:
				tail.next = list2
				list2 = list2.next
			tail = tail.next

		if list1:
			tail.next = list1
		elif list2:
			tail.next = list2	
			
		return dummy.next
```