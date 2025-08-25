---
description: Launch code-locator agent to find specific functionality
argument-hint: [what you're looking for]
---

# Code Locator Agent

Launch the code-locator subagent with pure context passthrough.

## Instructions:

Immediately launch the code-locator agent with:
- Current working directory context
- Recent conversation context (if relevant)
- User's exact request with NO interpretation

Do NOT:
- Interpret what the user wants to find
- Add search strategies or focus areas
- Expand or modify the user's request
- Provide guidance to the agent

Just pass through: environment context + user's actual words.

Launch code-locator agent with user request: $ARGUMENTS