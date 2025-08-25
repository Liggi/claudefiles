---
description: Launch codebase-mapper agent for architectural understanding
argument-hint: [question about how system works]
---

# Codebase Mapper Agent

Launch the codebase-mapper subagent with pure context passthrough.

## Instructions:

Immediately launch the codebase-mapper agent with:
- Current working directory context
- Recent conversation context (if relevant)
- User's exact request with NO interpretation

Do NOT:
- Interpret what the user wants to understand
- Add analysis frameworks or focus areas
- Expand or modify the user's request
- Provide guidance to the agent

Just pass through: environment context + user's actual words.

Launch codebase-mapper agent with user request: $ARGUMENTS