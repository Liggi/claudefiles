---
description: Launch adversarial-analysis agent for critical evaluation
argument-hint: [what to analyze/critique]
---

# Adversarial Analysis Agent

Launch the adversarial-analysis subagent with pure context passthrough.

## Instructions:

Immediately launch the adversarial-analysis agent with:
- Current working directory context
- Recent conversation context (if relevant)
- User's exact request with NO interpretation

Do NOT:
- Interpret what the user wants
- Add focus areas or analysis frameworks
- Expand or modify the user's request
- Provide guidance to the agent

Just pass through: environment context + user's actual words.

Launch adversarial-analysis agent with user request: $ARGUMENTS