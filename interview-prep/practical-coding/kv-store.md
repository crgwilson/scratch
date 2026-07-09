---
tags:
  - coding-exercise
  - interview-prep
  - practical-coding
---
# Key-value store (three staged variants)
## 1. Time-based KV store
### Setup
Build a key-value store where every write is timestamped, and reads can ask 'what was the value as of time T?
### Part 1a
```python
kv = TimeKVStore()
kv.set("model", "v1", timestamp=5)
kv.set("model", "v2", timestamp=10)
kv.get("model", timestamp=7)    # "v1"  (latest value at or before t=7)
kv.get("model", timestamp=10)   # "v2"
kv.get("model", timestamp=3)    # None / "" (nothing yet)
kv.get("missing", timestamp=99) # None
```
Timestamps for a given key are strictly increasing. Aim for O(log n) reads (`bisect`).
### Part 1b - Real clock + testability
Now `set(key, value)` uses the real current time. Questions you must answer in code or out loud:
* How do you unit test this? (Inject a clock / mock `time.time`.)
* How do you guarantee strictly increasing timestamps if two sets land on the same clock tick? (Monotonic counter tiebreaker or `time.monotonic_ns`.)
### Part 1c - Thread safety
Multiple threads call `set`/`get` concurrently. Make it correct. Then discuss:
* One global lock vs. per-key locks - when does each win?
* Would a read-write lock help here? What does Python actually give you?
* What does the GIL protect you from, and what doesn't it?
## 2. Versioned KV store
### Setup
Keys and values are arbitrary strings - they may contain newlines, commas, colons, quotes, anything. Persist the store to a file and restore it. **You may not use json, pickle, csv, or any serialization library.**
### Part 2a
`serialize() -> str` and `deserialize(s)` round-trip the whole store. The naive `key:value\n` format fails - why? Land on length-prefix encoding, e.g. `3:foo11:hello:world` (Redis-protocol style). Test with adversarial strings: `""`, `"5:"`, `"\n\n"`, `"3:abc"`.
## Part 2b
`save(path)` / `load(path)`.
## Part 2c
The store is too big for one file. Shard into fixed-size files (e.g., max N bytes each). How do you find which shard holds a key? (Hash-based assignment vs. an index/manifest file - discuss, implement one.)

**Verbal follow-ups:** crash mid-save (write-temp-then-rename), append-only log + compaction vs. full rewrite.