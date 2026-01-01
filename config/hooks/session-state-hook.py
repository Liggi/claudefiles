#!/usr/bin/env python3
"""
Session State Hook for Claude Code
Triggered on Stop - writes session summary to shared state.

Reads the session transcript to extract what was worked on.
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime

SHARED_STATE_FILE = Path.home() / "claudia" / "shared-state.jsonl"

def extract_session_summary():
    """
    Try to extract a summary from the session.

    Hook receives session info via stdin as JSON.
    """
    try:
        input_data = sys.stdin.read()
        if input_data.strip():
            data = json.loads(input_data)
            # The Stop hook receives session_id and transcript_path
            session_id = data.get("session_id", "unknown")
            transcript_path = data.get("transcript_path", "")

            # Could read transcript here to extract summary
            # For now, just note the session ended
            return {
                "session_id": session_id,
                "transcript_path": transcript_path,
            }
    except:
        pass

    return {}


def get_recent_work():
    """
    Heuristic: check recent git activity or file modifications
    to understand what was worked on.
    """
    cwd = os.getcwd()

    # Try git status
    try:
        import subprocess
        result = subprocess.run(
            ["git", "diff", "--stat", "HEAD~1", "HEAD"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            # Get just the summary line
            lines = result.stdout.strip().split('\n')
            if lines:
                return lines[-1]  # e.g., "3 files changed, 45 insertions(+)"
    except:
        pass

    return ""


def write_entry(source, summary, working_on="", context=None):
    """Write entry to shared state file."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "summary": summary,
        "working_on": working_on,
        "open_tasks": [],
        "blockers": [],
        "context": context or {},
    }

    SHARED_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(SHARED_STATE_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return entry


def main():
    cwd = os.getcwd()
    source = f"claude-code:{cwd}"

    session_info = extract_session_summary()
    recent_work = get_recent_work()

    summary = f"Session ended"
    if recent_work:
        summary += f" - {recent_work}"

    entry = write_entry(
        source=source,
        summary=summary,
        context=session_info
    )

    # Silent success - don't print to avoid cluttering session end


if __name__ == "__main__":
    main()
