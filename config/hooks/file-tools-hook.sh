#!/bin/bash

# Read JSON input from stdin
input=$(cat)

# Extract the command using jq
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# Check for cat command anywhere (but allow special cases like heredoc)
if [[ "$command" =~ [[:space:]]cat[[:space:]] ]] && [[ ! "$command" =~ \<\< ]]; then
    echo "Use 'bat' instead of 'cat' for better syntax highlighting and line numbers" >&2
    exit 2
fi

# Check for find command anywhere (but exclude gpt5-search)
if [[ "$command" =~ [[:space:]]find[[:space:]] ]] && [[ ! "$command" =~ gpt5-search ]]; then
    echo "Use 'fd' instead of 'find' for faster, cleaner syntax" >&2
    exit 2
fi

# Check for grep command anywhere
if [[ "$command" =~ [[:space:]]grep[[:space:]] ]]; then
    echo "Use 'rg' (ripgrep) instead of 'grep' for much faster search" >&2
    exit 2
fi

# Allow other commands to proceed
exit 0