---
description: Read ~/cui-debug.log for frontend debugging (browser + server logs)
argument-hint: [optional: "clear" to clear, "last N" for N lines, "rotate" to archive]
---

# Debug Log Reader

Read the cui-custom debug log file (`~/cui-debug.log`) which contains both browser console logs and server-side debug logs from the orchestrator dashboard.

## Instructions:

### Step 1: Check file size first
Run: `ls -la ~/cui-debug.log 2>/dev/null || echo "File does not exist"`

### Step 2: Auto-rotate if over 100KB
If the file exists and is over 100KB (100000 bytes), automatically rotate it:
1. Move current log to `~/cui-debug.log.1` (overwriting any existing .1 file)
2. Create fresh empty `~/cui-debug.log`
3. Report: "Log rotated (was X KB). Previous log saved to ~/cui-debug.log.1"

Commands for rotation:
```bash
mv ~/cui-debug.log ~/cui-debug.log.1 && touch ~/cui-debug.log
```

### Step 3: Handle arguments
- **"clear"**: Truncate the log file (`> ~/cui-debug.log`) and confirm
- **"rotate"**: Force rotation regardless of size (same as auto-rotate above)
- **"last N"** (e.g., "last 50"): Show only the last N lines
- **No argument**: Show the most recent entries (last 100 lines by default)

### Step 4: Read and analyze
1. Read the appropriate portion of the log
2. Analyze for errors, warnings, or relevant debugging information
3. Summarize key findings if the log is lengthy

## Context:

This log captures:
- **BROWSER logs**: Console warnings from the React frontend (prefixed with `[BROWSER]`)
- **SERVER logs**: Debug output from the Express backend (prefixed with `[SERVER]`)

Useful for debugging:
- Frontend rendering issues
- API request/response problems
- SSE stream events
- Insight system behavior

Now check the file size and proceed with the instructions above.
