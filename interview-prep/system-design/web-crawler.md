---
tags:
  - interview-prep
  - system-design
---
# Web Crawler at Scale

## Prompt
Design a crawling service: given seed URLs, crawl the web politely and store page content for downstream indexing. Target 100k pages/sec sustained. Must respect per-domain rate limits and robots.txt.

**Follow-up script:** 
* URL frontier design - how do you get both priority AND politeness?
* Dedup at 100k/sec - exact set vs. Bloom filter trade-off. Crawler traps (infinite calendars).
* A crawler node dies holding 10k in-flight URLs. Re-crawl scheduling (freshness).
* DNS becomes your bottleneck - now what? (Ties directly back to coding Q6 - have the small -> distributed story smooth in both directions.)