# Rate Limiter as a Service

## Prompt
Design a rate-limiting service other internal services call: `allow(customer_id, resource) -> yes/no`, with per-customer configurable limits. It must add <5ms latency and survive its own outages gracefully.

**Follow-up script:**
* Algorithm choice (token bucket vs. sliding window) and where counters live (Redis? in-process with sync?).
* The limiter service goes down - fail open or closed, and who decides?
* Distributed counters: a customer's traffic hits 20 API nodes - exact vs. approximate limiting trade-off.
* Hot key problem: one customer is 30% of traffic.