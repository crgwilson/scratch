# Spreadsheet with Formula Dependencies
## Setup
Build the engine behind a spreadsheet. Cells are named like A1, B2. A cell holds either an integer or a formula that sums other cells.
## Part A
```python
s = Spreadsheet()
s.set_cell("A1", "5")
s.set_cell("A2", "7")
s.set_cell("B1", "=A1+A2")
s.get_cell("B1")     # 12
s.set_cell("A1", "10")
s.get_cell("B1")     # 17
```
Formulas: `=X+Y+...` where each term is a cell ref or integer literal (`=A1+5+B2`). Lazy evaluation (compute on `get`) is fine here.
## Part B - Chained dependencies
`C1 = =B1+A1` where `B1` is itself a formula. Recursive evaluation with memoization within a single `get` call.
## Part C - Cycle detection
`s.set_cell("A1", "=B1")` when `B1 = "=A1"` -> raise an error, either at set time or get time (choose, justify).
## Part D - Make `get_cell` O(1)
Requirement change: reads vastly outnumber writes. Push work to `set_cell`: maintain a dependency graph (cell → dependents), and on write, propagate recomputation to all downstream cells in topological order. Discuss the cost model shift and when eager propagation loses (write-heavy, deep chains).

**Verbal follow-ups:** other operators (-, *), ranges (`=SUM(A1:A10)`), and how you'd detect cycles in the eager version (topo sort / DFS coloring).