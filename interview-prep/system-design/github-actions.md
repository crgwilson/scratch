# Multi-Tenant CI/CD System ("Design GitHub Actions")
Target: core design complete by minute 35, two deep dives, then scaling pressure.
## Prompt
Design a service where organizations define pipelines in config (build -> test -> deploy steps), triggered by code pushes.
* Runs execute in isolated environments.
* Thousands of orgs
* Spiky load.

**Follow-up script:**

Where do jobs run and how do you isolate tenants (containers? VMs? why)?

Scheduler design -
* Fairness across orgs when one org submits 10k jobs.
* A worker dies mid-job - what happens?
* Caching build artifacts across runs. How do you handle secrets?

Logs - 
* Streaming live to the browser while the job runs - design that path. (You've built much of this - practice presenting it as _derived from requirements_, not recalled.)