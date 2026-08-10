from mini_sql import execute


def test_select_columns_from_table_with_equality_where() -> None:
    tables = {
        "users": [
            {"id": 1, "name": "Ada", "role": "admin"},
            {"id": 2, "name": "Grace", "role": "user"},
            {"id": 3, "name": "Linus", "role": "admin"},
        ]
    }

    rows = execute("SELECT id, name FROM users WHERE role = 'admin'", tables)

    assert rows == [
        {"id": 1, "name": "Ada"},
        {"id": 3, "name": "Linus"},
    ]


def test_where_can_compare_numbers() -> None:
    tables = {
        "orders": [
            {"id": 1, "total": 20},
            {"id": 2, "total": 50},
        ]
    }

    assert execute("SELECT id FROM orders WHERE total = 50", tables) == [{"id": 2}]


# Part 2 - AND/OR
#
# def test_where_supports_and_or() -> None:
#     rows = execute(
#         "SELECT id FROM users WHERE role = 'admin' AND active = true",
#         tables,
#     )
#
#     assert rows == [{"id": 1}]
#
#
# Part 3 - ORDER BY and LIMIT
#
# def test_order_by_and_limit() -> None:
#     rows = execute("SELECT id FROM orders WHERE status = 'paid' ORDER BY total LIMIT 2", tables)
#
#     assert rows == [{"id": 3}, {"id": 1}]
#
#
# Part 4 - aggregates and GROUP BY
#
# def test_count_and_sum_group_by() -> None:
#     rows = execute("SELECT user_id, COUNT(*), SUM(total) FROM orders GROUP BY user_id", tables)
#
#     assert rows == [
#         {"user_id": 1, "count": 2, "sum_total": 75},
#         {"user_id": 2, "count": 1, "sum_total": 25},
#     ]
