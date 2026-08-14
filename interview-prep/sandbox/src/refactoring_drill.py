# P9 - Refactoring drill
#
# This file intentionally starts with rough legacy-style code instead of stubs.
# Practice goal:
# * set a 30-minute timer
# * improve naming
# * extract functions
# * add tests
# * fix the latent bug
# * narrate your choices as if pairing with an interviewer
#
# Keep the public function name and return shape stable while refactoring.
def order_report(rows: list[dict]) -> dict:
    x = {}
    y = 0
    z = 0
    for r in rows:
        if r.get("status") != "cancelled":
            y = y + 1
            z = z + r.get("total", 0)
            c = r.get("customer", "unknown")
            if c not in x:
                x[c] = 0
            x[c] = x[c] + r.get("total", 0)
    return {"count": y, "total": z, "by_customer": x}
