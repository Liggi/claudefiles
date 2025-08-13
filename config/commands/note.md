---
description: Set or clear statusline note
argument-hint: [note text] (leave empty to clear)
---

# Note Command

If arguments are provided, set the statusline note to the given text.
If no arguments are provided, clear the current note.

Please use the bash tool to either:
1. Write the note text to `~/.claude/note` if arguments are provided
2. Remove the `~/.claude/note` file if no arguments are provided

The note will appear in the statusline with a 📝 emoji.