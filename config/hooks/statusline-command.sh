#!/bin/bash

# Read JSON input from stdin
input=$(cat)

# Extract basic info
current_dir=$(echo "$input" | jq -r '.workspace.current_dir' | sed "s|$HOME|~|g")
model_name=$(echo "$input" | jq -r '.model.display_name')

# Get current date and time separately
current_date=$(date "+%b %d")
current_time=$(date "+%H:%M")

# Check for note file
note_content=""
note_file="$HOME/.claude/note"
if [[ -f "$note_file" && -s "$note_file" ]]; then
    note_content=$(cat "$note_file" | head -n 1)  # Get first line only
fi

# Build the status line parts
status_line="\033[32m🕐 $current_time\033[0m \033[90m|\033[0m \033[33m📅 $current_date\033[0m \033[90m|\033[0m \033[35m🤖 $model_name\033[0m \033[90m|\033[0m \033[36m📁 $current_dir\033[0m"

# Add note section if note exists
if [[ -n "$note_content" ]]; then
    status_line="$status_line \033[90m|\033[0m \033[94m📝 $note_content\033[0m"
fi

# Output the formatted status line with proper color interpretation
printf '%b' "$status_line"