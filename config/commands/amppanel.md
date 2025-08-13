# Amp Panel Research Partner

Use the amp panel as a research partner. Claude Code will send a research prompt to amp and receive the results back.

Usage: `/amppanel [task description]`

## Instructions:

1. Take the optional task description argument to focus the research
2. Analyze what Claude Code needs to research or investigate based on context and the task description
3. Create a focused research prompt for amp
4. Send the prompt to amp panel (pane 1) using the two-step reliable method:
   - First: `tmux send-keys -t 1 "your prompt here"`
   - Second: `tmux send-keys -t 1 C-m`
5. Always include return instructions in the prompt sent to amp (using the same two-step method)
6. Wait for and process amp's research results
7. Use the research findings to help with the current task

## Tmux Panel Setup:
- **Pane 1**: amp (research partner)
- **Pane 2**: Claude Code (current panel)  
- **Pane 3**: Neovim/Terminal

## Required Prompt Format:
Every prompt sent to amp must include these explicit instructions:

```
[Research request here]. When you have the results, send them back to me by executing these exact commands in sequence:
tmux send-keys -t 2 "Research Results: [your findings here]"
tmux send-keys -t 2 C-m

Note: Execute both commands - the first sends the text, the second presses Enter.
```

## Example Usage:
```bash
# Step 1: Send the prompt text
tmux send-keys -t 1 "Research the latest Next.js 15 app router patterns for nested layouts. When you have the results, send them back to me by executing these exact commands in sequence: tmux send-keys -t 2 'Research Results: [your findings here]' then tmux send-keys -t 2 C-m Note: Execute both commands - the first sends the text, the second presses Enter."

# Step 2: Submit the prompt
tmux send-keys -t 1 C-m
```

Now identify what needs to be researched based on the current conversation context and the provided task description, then send an appropriate prompt to amp using the two-step method.