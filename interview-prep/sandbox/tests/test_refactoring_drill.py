from refactoring_drill import order_report


def test_order_report_summarizes_non_cancelled_orders() -> None:
    rows = [
        {"customer": "Ada", "status": "paid", "total": 25},
        {"customer": "Grace", "status": "cancelled", "total": 100},
        {"customer": "Ada", "status": "paid", "total": 75},
        {"customer": "Linus", "status": "pending", "total": 50},
    ]

    assert order_report(rows) == {
        "count": 3,
        "total": 150,
        "by_customer": {"Ada": 100, "Linus": 50},
    }


def test_order_report_handles_missing_customer_and_total() -> None:
    rows = [
        {"status": "paid"},
        {"customer": "Ada", "status": "paid", "total": 10},
    ]

    assert order_report(rows) == {
        "count": 2,
        "total": 10,
        "by_customer": {"unknown": 0, "Ada": 10},
    }
