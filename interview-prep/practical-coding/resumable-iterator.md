# Resumable Iterator
## Setup
We work with very large datasets and long-running jobs that can be interrupted at any point. We want iterators whose position can be saved and restored, so a job can resume exactly where it left off. Here's an interface - do not change its signature:
```python
class ResumableIterator:
    def __iter__(self): ...
    def __next__(self): ...          # raises StopIteration when exhausted
    def get_state(self): ...         # returns an opaque state object
    def set_state(self, state): ...  # restores iterator to a previously saved state
```
Note: do not assume the state is an integer index. Callers treat it as opaque. There is no `has_next()`.
## Part A - Write the tests first
Before implementing anything, write a generic test function `test_iterator(make_iter, expected_elements)` that validates ANY implementation of this interface. It should:
* Iterate through, capturing `get_state()` before each `next()` call.
* For every captured state, create/reset an iterator, `set_state(state)`, consume to the end, and assert the remaining elements match the expected suffix.
* Cover: state captured at the very start, mid-iteration, and at exhaustion; and correct StopIteration behavior.
## Part B - List Iterator
Implement `ResumableListIterator(items: list)` conforming to the interface. Your Part A tests must pass unmodified.

Example:
```python
it = ResumableListIterator([1, 2, 3, 4])
next(it)            # 1
s = it.get_state()
next(it)            # 2
next(it)            # 3
it.set_state(s)
next(it)            # 2  (resumes from saved point)
```
## Part C - Multi-file iterator by composition
You're given (assume it exists and works) `ResumableFileIterator(path)` that conforms to the interface and yields records from a single JSON-lines file. Implement `ResumableMultiFileIterator(paths: list[str])` that iterates all records across all files in order, using the single-file iterator internally.

Requirements:
- Must conform to the same interface; your Part A tests must pass unmodified.
- Must handle empty files anywhere in the list (including first and last).
- Think carefully about what `get_state()` must contain (hint: file position + inner state) and what `set_state()` must reconstruct.

For practice without real files, stub: `ResumableFileIterator = ResumableListIterator` over per-file lists.
## Part D - Async version (stretch)
Convert the multi-file iterator to `async` (`__anext__`, `async for`) so file reads don't block. Discuss where state capture gets tricky with in-flight reads.

**Verbal follow-ups:**
* What if a file is modified between `get_state()` and `set_state()`?
* How would you make the state serializable to disk (job resumes in a new process)?
* Extend to a 2D case: an iterator over a list of lists, still resumable.