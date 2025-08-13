# Global Claude Instructions

## Web Search Strategy
**For comprehensive research tasks requiring depth, citations, and recent information:**
- Use the custom `gpt5-search` script via: `gpt5-search "detailed prompt"`
- Provides superior depth, structured analysis, comprehensive source citations, and recent content
- ~4.6k token cost but delivers research-quality results with proper attribution
- Best for: technical documentation research, framework comparisons, architectural decisions

**For quick lookups and simple queries:**
- Use built-in WebSearch tool for speed and efficiency
- Nearly instant results with minimal token usage
- Best for: quick facts, simple clarifications, basic information gathering

**When using the custom web search script, ALWAYS write proper prompts:**

**WRONG (Search Query Style):**
- "How to configure Claude Code hooks"
- "Latest Claude Code documentation" 

**CORRECT (Prompt Style):**
- "I need to understand how to configure Claude Code hooks. Please search the web for the latest official documentation and provide detailed setup instructions with examples."
- "Please search the web for current Claude Code documentation and explain the latest features and configuration options available."

**Required Elements for Custom Script:**
- Always start with "I need..." or "Please search the web for..."
- Explicitly request web searching in every prompt
- Ask for comprehensive answers, examples, or explanations
- Remember: You are instructing another LLM that has web search capabilities

## Multi-Tool Workflow Guidelines
**When using research tools followed by planning/analysis tools:**

**CRITICAL**: Always pass research findings explicitly to downstream tools. Never assume context will carry over.

**Research → Planning Agent Pattern:**
1. Use `gpt5-search` to gather current information
2. **MUST include full research results** in planning agent prompt using this format:
```
## RESEARCH CONTEXT - LATEST PATTERNS/REQUIREMENTS:
[Insert complete gpt5-search results here]

[Then continue with the planning request]
```

**Common Failure Pattern to Avoid:**
- ❌ "Based on my research..." (vague reference)
- ❌ "I found that..." (no actual data provided)
- ✅ Include the complete research output in structured format

**Why This Matters:**
- Each tool call is stateless - tools don't automatically share context
- Research findings are only valuable if explicitly passed to tools that need them
- Planning agents are designed to receive research context but won't work without it

## Path Aliases
- "dotfiles" = `/Users/jasonliggi/dotfiles`
- "claudefiles" = `/Users/jasonliggi/claudefiles`

## GitHub CLI Tips
**Finding PR Comments:**
- `gh pr view <number> --comments` - Shows general PR comments only
- `gh api repos/<owner>/<repo>/pulls/<number>/comments` - Shows inline review comments (line-specific)
- `gh pr view <number> --json reviews` - Shows review summaries (but not inline comment bodies)

**Why this matters:** Inline review comments (the ones you see when reviewing specific lines of code) don't appear in the standard `--comments` output and require the API call to retrieve.

## Commit Guidelines
- NEVER add "> Generated with [Claude Code]" or "Co-Authored-By: Claude" to commit messages
- Use clean, standard commit messages without Claude Code attribution
- Use conceptual category tags like [tooling], [config], [docs] etc.
- Keep commit messages as one-liners: "[category] brief description"