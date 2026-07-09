---
tags:
  - interview-prep
  - system-design
---
# Design ChatGPT (product/full-stack emphasis)
Target: core design complete by minute 35, two deep dives, then scaling pressure.
## Prompt
Design a chat application backed by an LLM: user sends a message, the model's reply streams back token by token. Conversations persist.

Start with the MVP for 100k users, we'll scale from there. Sketch the client too.

**Follow-up script:**
* SSE vs WebSockets - pick and defend.
* The stream dies at token 200 - what does the client show, and can it resume?
* Where does conversation history live and what's the schema?
* The model takes 30s worst-case - how does that shape timeouts everywhere in the chain? 

Now 100M users:
* What's stateless and what isn't?
* Rate limiting per user. How do you show "the model is typing" honestly?