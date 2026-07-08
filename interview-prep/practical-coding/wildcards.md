# Wildcards (one timed rep each if you have time)

## 8a. Version-support detective problem (hidden-requirements style)
You're given a list of dependency version strings, e.g. `["103.003.02", "103.003.03", "203.003.02"]`, and a predicate `supports_feature(version) -> bool` (or a table of observed data). Return the earliest version that supports the current feature.

**The catch:** the provided test cases progressively contradict your assumptions (e.g., a later version _loses_ support; version segments compare numerically not lexically; different major lines behave independently). The real skill tested: **read each test case, form a hypothesis, confirm the new rule with the interviewer out loud, and refactor without breaking earlier cases.** Practice by having a friend (or AI) invent 2 surprise rule changes mid-solve.
## 8b. Meeting rooms / interval scheduler
Given meeting intervals `[(start, end), ...]`, (A) can one person attend all? (B) minimum rooms needed? (C) implement `book(start, end)` that rejects double-bookings on one room (LC 729 MyCalendar). Min-heap of end times for B; sorted list + bisect for C.
## 8c. IP address iterator
Implement an iterator over every IPv4 address in a CIDR range, e.g. `IPRange('192.168.0.0/30')` yields .0 through .3. Don't materialize the list (a /8 is 16M addresses).

Extensions: skip network/broadcast addresses; make it resumable (combines with Q1); support multiple disjoint ranges.
## 8d. Refactoring rep
Take any ~80-line working-but-ugly Python snippet (grab one of your own old scripts, or generate one: global state, one giant function, magic strings, no error handling).

25 minutes: make it production-quality - small functions, names, exceptions, tests - while narrating what you're fixing and why. The narration is the skill.