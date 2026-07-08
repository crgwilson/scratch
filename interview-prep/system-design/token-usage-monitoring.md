# Token Usage Monitoring / Metrics System

## Prompt
Every API request consumes tokens. Design the system that tracks usage per customer in near-real-time, powers a usage dashboard, enforces monthly quotas, and feeds billing. Millions of customers, ~1M requests/sec.

**Follow-up script:**
* Counting path: can you afford a synchronous DB write per request? (Aggregation windows, write-behind.)
* Quota enforcement needs to be fast AND roughly correct - where does the check live and how stale can it be?
* A customer disputes their bill - what's your source of truth vs. your fast path?
* Late/duplicate events. Dashboard query patterns vs. billing query patterns - one store or two?