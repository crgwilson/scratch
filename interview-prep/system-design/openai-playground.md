# Design the OpenAI Playground (mockup -> product)

## Prompt
Here's a rough mockup: a left pane of saved conversation threads, a main pane showing the current thread with a prompt box, and a settings drawer (model, temperature).

Design the full stack: the API between client and server, the data model, and the backend. Then tell me how you'd evolve it for teams sharing threads.

**Follow-up script:**
Enumerate the actual endpoints and their request/response shapes. Optimistic UI: the user hits send - what renders before the server confirms? Schema for threads/messages - show the tables. Pagination of long threads. Two browser tabs open on the same thread - what happens? Team sharing: authz model and what changes in the schema.