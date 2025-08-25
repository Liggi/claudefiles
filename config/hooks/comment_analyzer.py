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
            r'(?<!:)//\s*(.+)$',      # C++, JS, Java style - not preceded by :
            r'(?<!\$)#\s*(.+)$',       # Python, Shell style - not preceded by $ - exclude URLs
            r'^\s*--\s*(.+)$',  # SQL, Haskell style - must start line
        ],
        'multi_line': [
            r'\{\s*/\*\s*(.+?)\s*\*/\s*\}',  # JSX comments (check first)
            r'/\*\s*(.+?)\s*\*/',     # C style block comments
            r'"""(.+?)"""',           # Python docstrings
            r"'''(.+?)'''",           # Python docstrings
        ]
    }
    
    def is_inside_string(line, pos):
        before_pos = line[:pos]
        single_quotes = before_pos.count("'") - before_pos.count("\\'")
        double_quotes = before_pos.count('"') - before_pos.count('\\"')
        
        # Skip content inside print/log functions to avoid flagging debug output
        if re.search(r'\b(print|console\.log|printf|puts|echo)\s*\(', line[:pos]):
            return True
            
        return (single_quotes % 2 == 1) or (double_quotes % 2 == 1)
    
    for i, line in enumerate(lines, 1):
        original_line = line
        line_stripped = line.strip()
        
        # Skip shebang lines (#!/...)
        if line_stripped.startswith('#!'):
            continue
            
        # Check if next line looks like a struct field declaration
        next_line = lines[i] if i < len(lines) else None
        is_struct_field = bool(re.match(r'^\s+\w+\s+[\w\*\[\]\.]+.*$', next_line or ''))
        
        # Skip struct field comments - they document API contracts
        if is_struct_field:
            continue
        
        for pattern in patterns['single_line']:
            match = re.search(pattern, line)
            if match:
                match_pos = match.start()
                if is_inside_string(line, match_pos):
                    continue
                
                comment_text = match.group(1).strip()
                if comment_text:
                    # Skip commented-out code blocks
                    if re.match(r'^(vim\.|local |function |if |for |while |return |end|}).*', comment_text):
                        continue
                    
                    # Skip single-line code statements  
                    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*[=\(].*', comment_text):
                        continue
                        
                    with open('/tmp/hook_debug.log', 'a') as f:
                        f.write(f"Line {i}: '{original_line}' -> '{comment_text}'\n")
                    comments.append({
                        'line': i,
                        'text': comment_text,
                        'type': 'single_line',
                        'full_line': original_line
                    })
                break
    
    # Process multi-line comments including JSX comments
    full_content = '\n'.join(lines)
    matched_ranges = []
    
    for pattern in patterns['multi_line']:
        matches = re.finditer(pattern, full_content, re.DOTALL)
        for match in matches:
            overlaps = any(
                (match.start() < end and match.end() > start) 
                for start, end in matched_ranges
            )
            if overlaps:
                continue
                
            comment_text = match.group(1).strip()
            if comment_text:
                start_pos = match.start()
                line_num = full_content[:start_pos].count('\n') + 1
                matched_ranges.append((match.start(), match.end()))
                comments.append({
                    'line': line_num,
                    'text': comment_text,
                    'type': 'multi_line',
                    'full_line': lines[line_num - 1] if line_num <= len(lines) else ''
                })
    
    return comments

def analyze_comments_with_gpt5(comments, code_context):
    """Use GPT-5-mini to analyze if comments are redundant or useful."""
    if not comments:
        return []
    
    # Prepare the prompt for GPT-5-mini
    comments_text = "\n".join([f"Line {c['line']}: {c['text']}" for c in comments])
    
    prompt_content = [
        "Analyze these comments to determine if they are REDUNDANT or USEFUL.",
        "",
        "Code context:",
        "```",
        code_context,
        "```",
        "",
        "Comments:",
        comments_text,
        "",
        "REDUNDANT comments:",
        "- State the obvious from reading code",
        "- Talk about how things used to work or what changed (\"instead of\", \"rather than\", \"used to\", \"changed from\", \"previously\", \"now we\", \"unlike before\")",
        "- Reference other codebase parts that may change over time",
        "",
        "USEFUL comments:",  
        "- Explain WHY (business logic, constraints, requirements)",
        "- Document non-obvious behavior or edge cases",
        "- Improve glanceability of complex logic",
        "- Contain actionable info (TODOs, warnings, performance notes)",
        "",
        "CRITICAL: Comments should only describe the current code. Any mention of old approaches, previous states, or what changed makes a comment REDUNDANT.",
        "",
        "Respond with JSON:",
        '{"analysis": [{"line": <number>, "comment": "<text>", "category": "REDUNDANT"|"USEFUL", "reason": "<brief explanation>"}]}'
    ]
    prompt = "\n".join(prompt_content)

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

    new_content = ""
    if tool_name == "Edit":
        new_content = tool_input.get("new_string", "")
        old_content = tool_input.get("old_string", "")
        if old_content in new_content:
            new_content = new_content.replace(old_content, "", 1).strip()
    elif tool_name == "MultiEdit":
        edits = tool_input.get("edits", [])
        truly_new_content = []
        for edit in edits:
            new_str = edit.get("new_string", "")
            old_str = edit.get("old_string", "")
            if old_str == "":
                truly_new_content.append(new_str)
            elif old_str not in new_str:
                truly_new_content.append(new_str)
        new_content = "\n".join(truly_new_content)
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