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


```python
# DESCRIPTION
# Build an in-memory database that supports SQL-like operations including INSERT, SELECT with WHERE clauses, and ORDER BY functionality. Implement efficient data storage structures, a query parser to evaluate conditions, and inverted indexes to optimize search performance. For example, after inserting records like {id: 1, name: 'Alice', age: 30}, you should be able to query SELECT * WHERE age > 25 ORDER BY name and retrieve matching records efficiently.
# 
# Input:
# 
# INSERT {id: 1, name: 'Alice', age: 30}
# INSERT {id: 2, name: 'Bob', age: 25}
# SELECT * WHERE age > 25 ORDER BY name ASC
# Output:
# 
# [{id: 1, name: 'Alice', age: 30}]
# 
# Explanation: Only Alice matches the condition age > 25, returned in ascending order by name
# 
# Constraints:
# 
# Support INSERT operations with arbitrary key-value pairs
# Support SELECT with multiple WHERE conditions (AND logic)
# Support ORDER BY with ASC/DESC sorting on any field
# Implement inverted indexes for efficient field-based lookups
# Handle comparison operators: =, !=, <, >, <=, >=
# Records can have different schemas (flexible fields)
import re

from enum import StrEnum
from typing import Any, NamedTuple

class Table:
    def __init__(self) -> None:
        self.records = []
        self.indexes = {}

    def insert(self, record: dict[str, Any]) -> None:
        record_idx = len(self.records)
        self.records.append(record)
        for field in record:
            if field not in self.indexes:
                self.indexes[field] = {}

            val = record[field]
            if val not in self.indexes[field]:
                self.indexes[field][val] = [record_idx]
            else:
                self.indexes[field][val].append(record_idx)


class QueryOperator(StrEnum):
    EQ = "="
    NE = "!="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="


class QueryClause(NamedTuple):
    col: str
    op: QueryOperator
    val: Any

    def evaluate(self, val: Any) -> bool:
        match self.op:
            case QueryOperator.EQ:
                return val == self.val
            case QueryOperator.NE:
                return val != self.val
            case QueryOperator.GT:
                return val > self.val
            case QueryOperator.GTE:
                return val >= self.val
            case QueryOperator.LT:
                return val < self.val
            case QueryOperator.LTE:
                return val <= self.val


class OrderDirection(StrEnum):
    ASC = "ASC"
    DESC = "DESC"


class QueryOrder(NamedTuple):
    col: str
    direction: OrderDirection


class Query(NamedTuple):
    cols: list[str]
    clauses: list[QueryClause]
    order_by: QueryOrder | None

class QueryParser:
    _CLAUSE_RE = re.compile(
        r"^\s*SELECT\s+(?P<columns>.+?)"
        r"(?:\s+WHERE\s+(?P<where>.+?))?"
        r"(?:\s+ORDER\s+BY\s+(?P<order_by>.+?))?"
        r"\s*;?\s*$",
        re.IGNORECASE | re.DOTALL,
    )

    _CONDITION_RE = re.compile(
        r"\s*(?P<column>\w+)\s*(?P<operator>=|!=|<>|<=|>=|<|>)\s*(?P<value>.+?)\s*$"
    )

    def parse(self, query_str: str) -> Query:
        match = self._CLAUSE_RE.match(query_str)
        if not match:
            raise ValueError("Cannot parse invalid query!")

        # SELECT
        columns_raw = match.group("columns").strip()
        columns = []
        if columns_raw == "*":
            columns.append("*")
        else:
            for c in columns_raw.split(","):
                columns.append(c.strip())

        # WHERE
        clauses = []
        if match.group("where"):
            where_raw = match.group("where")
            if "AND" in where_raw:
                for part in where_raw.split("AND"):
                    clauses.append(self._parse_clause(part))
            else:
                clauses.append(self._parse_clause(where_raw))

        # ORDER BY
        order_by: tuple[str, str] | None = None
        if match.group("order_by"):
            order_by_raw = match.group("order_by").split(" ")
            if order_by_raw[1] != "ASC" and order_by_raw[1] != "DESC":
                raise ValueError("Unable to parse invalid ORDER BY clause!")
            order_by = QueryOrder(col=order_by_raw[0], direction=order_by_raw[1])

        return Query(
            cols=columns,
            clauses=clauses,
            order_by=order_by,
        )


    def _parse_clause(self, clause_str: str) -> QueryClause:
        clause_match = self._CONDITION_RE.match(clause_str)
        if not clause_match:
            raise ValueError("Could not parse WHERE clause for invalid query!")

        val = clause_match.group("value")
        if isinstance(val, str):
            if val.isdigit():
                val = int(val)
            else:
                val = val.replace("'", "").replace("\"", "")

        return QueryClause(
            col=clause_match.group("column"),
            op=QueryOperator(clause_match.group("operator")),
            val=val,
        )


class QueryExecutor:
    def __init__(self, table: Table, parser: QueryParser) -> None:
        self.table = table
        self.parser = parser

    def execute(self, query: Query) -> list[dict[str, Any]]:
        ...


class InMemoryDatabase:
    def __init__(
        self,
        table: Table,
        parser: QueryParser,
        executor: QueryExecutor,
    ) -> None:
        self.table = table
        self.parser = parser
        self.executor = executor

    def insert(self, record: dict[str, Any]) -> None:
        self.table.insert(record)

    def query(self, query_str: str) -> list[dict[str, Any]]:
        parsed_query = self.parser.parse(query_str)
        return self.executor.execute(parsed_query)
```