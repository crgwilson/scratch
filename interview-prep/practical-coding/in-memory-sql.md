---
tags:
  - coding-exercise
  - interview-prep
  - practical-coding
---
# In-Memory SQL-Like Database
## Setup
Implement a simple in-memory database. No SQL parsing - just provide a programmatic API. One table is fine to start. All you need is what I ask for in each part; keep the API backward compatible as we extend it.
## Part A - Create, insert, project
```python
db = Database()
db.create_table("employees", ["id", "name", "age", "dept"])
db.insert("employees", ["1", "Ada", "36", "eng"])
db.insert("employees", ["2", "Grace", "45", "eng"])
db.insert("employees", ["3", "Alan", "41", "research"])

db.select("employees", ["name", "age"])
# [["Ada", "36"], ["Grace", "45"], ["Alan", "41"]]
```
* Inserting a row with the wrong number of values should raise an error.
* Selecting an unknown column should raise an error.
## Part B - WHERE, single condition (equality)
```python
db.select("employees", ["name"], where=[("dept", "=", "eng")])
# [["Ada"], ["Grace"]]
```
Empty result -> empty list. `where=None` -> all rows (backward compatible).
## Part C - Multi-condition WHERE + comparison operators
Support a list of conditions combined with AND, and operators `=`, `>`, `<`:
```python
db.select("employees", ["name"],
          where=[("dept", "=", "eng"), ("age", ">", "40")])
# [["Grace"]]
```
Decide and state out loud: are comparisons string or numeric? (Pick one, be consistent, mention the trade-off.)
## Part D - ORDER BY, single then multi-column, asc/desc
```python
db.select("employees", ["name", "age"],
          order_by=[("age", "desc")])
db.select("employees", ["name"],
          where=[("dept", "=", "eng")],
          order_by=[("dept", "asc"), ("age", "desc")])
```
Tie-break: stable within equal keys. Handle a row missing a sort value if your design allows sparse rows (treat as `""` or document your choice).

**Verbal follow-ups:**
* No code: how would you add an index to speed up equality WHERE? (hash index: column value → row ids). Range WHERE? (sorted list / tree + binary search). What are the write-time costs?
* How would you support OR?
* How does your design change for multiple tables? For a simple JOIN?