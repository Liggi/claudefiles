#!/bin/bash

# Read JSON input from stdin
input=$(cat)

# Extract the command using jq
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# Check for git add anywhere in the command
if [[ "$command" =~ git[[:space:]]+add ]]; then
    echo "Use 'gt add' instead of 'git add'" >&2
    exit 2
fi

# Check for git commit anywhere in the command
if [[ "$command" =~ git[[:space:]]+commit ]]; then
    echo "Use 'gt create -m \"commit message\"' instead of 'git commit'. Remember to run 'gt add' first to stage files." >&2
    exit 2
fi

# Check for git show (but allow git show | delta)
# Skip check if delta is configured as pager
if [[ "$command" =~ git[[:space:]]+show[[:space:]] ]] && [[ ! "$command" =~ \|[[:space:]]*delta ]]; then
    # Check if delta is configured as the pager for show
    if ! git config pager.show | grep -q delta; then
        echo "Use 'git show | delta' instead of plain 'git show' for better diff visualization" >&2
        exit 2
    fi
fi

# Check for git diff (but allow git diff | delta)
# Skip check if delta is configured as pager
if [[ "$command" =~ git[[:space:]]+diff ]] && [[ ! "$command" =~ \|[[:space:]]*delta ]]; then
    # Check if delta is configured as the pager for diff
    if ! git config pager.diff | grep -q delta; then
        echo "Use 'git diff | delta' instead of plain 'git diff' for better diff visualization" >&2
        exit 2
    fi
fi

# Check for git log (suggest git-graph for analysis)
if [[ "$command" =~ git[[:space:]]+log ]] && [[ ! "$command" =~ --oneline ]]; then
    echo "Use 'git-graph' instead of 'git log' for visual history analysis" >&2
    exit 2
fi

# Allow other commands to proceed
exit 0