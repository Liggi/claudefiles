#!/usr/bin/env python3
"""
Claude Code PreToolUse hook for analyzing and blocking redundant comments in code edits.
Uses GPT-5-mini to identify comments that don't provide useful contextual information.
"""

import json
import sys
import subprocess
import tempfile
import os
import re

def extract_comments_from_code(code, language=None):
    """Extract comments from code based on language patterns."""
    comments = []
    lines = code.split('\n')
    
    # Common comment patterns
    patterns = {
        'single_line': [
            r'//\s*(.+)$',      # C++, JS, Java style
            r'#\s*(.+)$',       # Python, Shell style
            r'^\s*--\s*(.+)$',  # SQL, Haskell style - must start line
        ],
        'multi_line': [
            r'/\*\s*(.+?)\s*\*/',  # C style block comments
            r'"""(.+?)"""',        # Python docstrings
            r"'''(.+?)'''",        # Python docstrings
        ]
    }
    
    def is_inside_string(line, pos):
        """Check if position is inside a string literal."""
        # Simple check for common string delimiters before the position
        before_pos = line[:pos]
        single_quotes = before_pos.count("'") - before_pos.count("\\'")
        double_quotes = before_pos.count('"') - before_pos.count('\\"')
        return (single_quotes % 2 == 1) or (double_quotes % 2 == 1)
    
    for i, line in enumerate(lines, 1):
        original_line = line
        line_stripped = line.strip()
        
        for pattern in patterns['single_line']:
            match = re.search(pattern, line)
            if match:
                # Check if this match is inside a string literal
                match_pos = match.start()
                if is_inside_string(line, match_pos):
                    continue
                
                comment_text = match.group(1).strip()
                if comment_text:
                    with open('/tmp/hook_debug.log', 'a') as f:
                        f.write(f"Line {i}: '{original_line}' -> '{comment_text}'\n")
                    comments.append({
                        'line': i,
                        'text': comment_text,
                        'type': 'single_line',
                        'full_line': original_line
                    })
                break
    
    # For multi-line comments, we'd need more sophisticated parsing
    # For now, focus on single-line comments which are most common
    return comments

def analyze_comments_with_gpt5(comments, code_context):
    """Use GPT-5-mini to analyze if comments are redundant or useful."""
    if not comments:
        return []
    
    # Prepare the prompt for GPT-5-mini
    comments_text = "\n".join([f"Line {c['line']}: {c['text']}" for c in comments])
    
    prompt = f"""You are a code quality analyzer. Analyze the following comments in the context of the surrounding code to determine if they are redundant or provide useful information.

Code context:
```
{code_context}
```

Comments to analyze:
{comments_text}

For each comment, determine if it is:
1. REDUNDANT: States the obvious or duplicates what the code clearly shows
2. USEFUL: Provides context, explains why (not what), documents complex logic, or adds valuable information

Respond with JSON format:
{{
    "analysis": [
        {{
            "line": <line_number>,
            "comment": "<comment_text>",
            "category": "REDUNDANT" | "USEFUL",
            "reason": "<brief explanation why it's redundant or useful>"
        }}
    ]
}}

Examples of REDUNDANT comments:
- "// Initialize the database connection" above db = new Database()
- "// Create user object with email and name" above user = new User(email, name)
- "// Check if user exists in the system" above if (userExists(id))

Examples of USEFUL comments:
- "// Workaround for API bug in v2.1"
- "// Performance optimization: cache results for 5 minutes"
- "// TODO: Replace with new authentication system"
"""

    try:
        # Use gpt5-mini command
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
            tmp_file.write(prompt)
            tmp_file.flush()
            
            # Run gpt5-mini command
            result = subprocess.run(
                ['gpt5-mini', '-f', tmp_file.name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Clean up temp file
            os.unlink(tmp_file.name)
            
            if result.returncode == 0:
                # Parse the JSON response
                try:
                    response = json.loads(result.stdout.strip())
                    return response.get('analysis', [])
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract from text response
                    return parse_text_response(result.stdout, comments)
            else:
                print(f"GPT-5-mini error: {result.stderr}", file=sys.stderr)
                return []
                
    except subprocess.TimeoutExpired:
        print("GPT-5-mini analysis timed out", file=sys.stderr)
        return []
    except FileNotFoundError:
        print("gpt5-mini command not found. Please ensure it's installed and in PATH", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error running GPT-5-mini analysis: {e}", file=sys.stderr)
        return []

def parse_text_response(text_response, comments):
    """Fallback parser for non-JSON responses."""
    analysis = []
    lines = text_response.split('\n')
    
    for comment in comments:
        # Simple heuristic: look for redundant patterns
        comment_lower = comment['text'].lower()
        redundant_patterns = [
            'increment', 'decrement', 'set', 'get', 'return',
            'loop', 'iterate', 'check if', 'assign'
        ]
        
        is_redundant = any(pattern in comment_lower for pattern in redundant_patterns)
        
        analysis.append({
            'line': comment['line'],
            'comment': comment['text'],
            'category': 'REDUNDANT' if is_redundant else 'USEFUL',
            'reason': 'Fallback heuristic analysis'
        })
    
    return analysis

def main():
    try:
        # Read input from Claude Code
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Skip non-file-modification tools since they don't introduce code comments
    if tool_name not in ["Edit", "MultiEdit", "Write"]:
        sys.exit(0)

    # Skip markdown files - they use # for headers, not comments
    file_path = tool_input.get("file_path", "")
    if file_path.endswith(('.md', '.markdown')):
        sys.exit(0)

    # Extract the new code content
    new_content = ""
    if tool_name == "Edit":
        new_content = tool_input.get("new_string", "")
    elif tool_name == "MultiEdit":
        # For MultiEdit, check all edits
        edits = tool_input.get("edits", [])
        new_content = "\n".join([edit.get("new_string", "") for edit in edits])
    elif tool_name == "Write":
        new_content = tool_input.get("content", "")

    if not new_content:
        sys.exit(0)

    comments = extract_comments_from_code(new_content)
    
    if not comments:
        sys.exit(0)  # No comments to analyze

    # Analyze comments with GPT-5-mini
    analysis = analyze_comments_with_gpt5(comments, new_content)
    
    # Check for redundant comments
    redundant_comments = [
        item for item in analysis 
        if item.get('category') == 'REDUNDANT'
    ]
    
    if redundant_comments:
        # Block the edit and provide feedback
        error_message = "🚫 Edit blocked: Redundant comments detected\n\n"
        error_message += "The following comments don't provide useful contextual information:\n\n"
        
        for comment in redundant_comments:
            error_message += f"  Line {comment['line']}: \"{comment['comment']}\"\n"
            error_message += f"    Reason: {comment['reason']}\n\n"
        
        error_message += "Please remove or improve these comments to provide more meaningful context.\n"
        error_message += "Good comments explain WHY, not WHAT the code does."
        
        print(error_message, file=sys.stderr)
        sys.exit(2)  # Block the tool execution
    
    # If no redundant comments found, allow the edit
    sys.exit(0)

if __name__ == "__main__":
    main()