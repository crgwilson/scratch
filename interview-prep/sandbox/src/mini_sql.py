# P5 - Mini SQL / expression evaluator
#
# Part 1:
# * parse SELECT col1, col2 FROM table WHERE col = value over a list of dicts.
#
# Part 2:
# * add AND/OR.
#
# Part 3:
# * add ORDER BY and LIMIT.
#
# Part 4:
# * add aggregates (COUNT, SUM) with GROUP BY.
#
# Part 5:
# * add INNER JOIN support across two in-memory tables.
#
# Part 6:
# * add a simple window function, such as ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...).
#
# This problem rewards structure. Keep tokenizer, parser, and executor separate.
class Tokenizer:
    def tokenize(self, query: str) -> list[str]:
        raise NotImplementedError


class Parser:
    def parse(self, query: str):
        raise NotImplementedError


class Executor:
    def execute(self, parsed_query, tables: dict[str, list[dict]]) -> list[dict]:
        raise NotImplementedError


def execute(query: str, tables: dict[str, list[dict]]) -> list[dict]:
    raise NotImplementedError
