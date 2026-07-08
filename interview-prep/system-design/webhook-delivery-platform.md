# Webhook Delivery Platform
Target: core design complete by minute 35, two deep dives, then scaling pressure.
## Prompt
We let customers register webhook URLs, and we need to deliver events to them - think Stripe's webhooks.

Design the platform: registration, delivery, retries, and visibility for customers into what happened. Assume 50k customer endpoints and 10k events/sec at peak.

**Follow-up script:**

An endpoint is down for 6 hours -
* What happens to its events?
* How do you guarantee at-least-once without hammering healthy endpoints when one is slow (head-of-line blocking)?
* Idempotency on the receiver side - what do you give them?
* A customer says "I never got event X" - walk me through debugging with your design.

Now 100x event volume -
* What breaks first?
* How do you stop a malicious/broken endpoint from consuming all delivery capacity?