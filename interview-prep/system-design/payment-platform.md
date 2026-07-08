# Payments Pipeline

## Prompt
Design a payment system: we authorize a charge with an external processor at purchase time, hold funds, and batch-settle daily. The processor is flaky - timeouts and ambiguous failures happen. Correctness is non-negotiable.

**Follow-up script:**
* The processor call times out - did the charge happen or not?
* Walk through your state machine.
* Idempotency keys - who generates them and where are they checked?
* Daily settlement job fails halfway - recovery?
* Reconciliation: our records vs. the processor's report disagree - design the process.
* Exactly-once - is it achievable? What do you actually promise?