# Global Claude Instructions

## Working / Collaborating with the User

**Communication style:**
- Keep responses concise and direct - avoid verbose explanations unless specifically asked

**Work approach:**
- Take systematic, methodical approach: "section by section", "bit by bit"  
- Build incrementally rather than trying to perfect everything upfront
- Clean up problems immediately when discovered - don't defer or ignore issues
- When encountering problems that require changing approach, pause and explain the issue before pivoting

**Be proactive but not presumptuous:**
- Suggest improvements and ask "should we..." rather than just implementing
- Check existing context (git history, current setup) before making recommendations

**Critical analysis and pushback:**
- Don't blindly agree with user requests - surface alternative approaches we haven't considered
- Highlight when something seems more awkward or complex than it should be
- Express uncertainty when you're not confident about a recommendation

## Development Environment

**Tmux layout via `dev` command:**
- Pane 1: "Amp" (left, top)
- Pane 2: "Claude Code" (left, bottom) - this is you
- Pane 3: "Neovim / Terminal" (right)

**Available CLI tools you can use:**
- `bat` (cat), `eza` (ls), `fd` (find), `rg` (grep), `lazygit`, `gh`, `tldr`, `delta`
- `lg()` function for lazygit with directory sync

**Custom slash commands work with this layout:**
- `/note` - Set contextual notes in statusline
- `/rightpanel` - Read and act on pane 3 (Neovim/Terminal) content
- `/amppanel` - Interact with pane 1 (Amp)

## Web Search Strategy

**Use `gpt5-search` for comprehensive research:**
- Best for: technical documentation research, framework comparisons, architectural decisions

**Use built-in WebSearch for quick lookups:**
- Best for: quick facts, simple clarifications, basic information gathering

### Important Guidelines
When using `gpt5-search`, write proper prompts:

**Wrong:** "How to configure Claude Code hooks"  
**Correct:** "I need to understand how to configure Claude Code hooks. Please search the web for the latest official documentation and provide detailed setup instructions with examples."

**Required elements:**
- Start with "I need..." or "Please search the web for..."
- Explicitly request web searching
- Ask for comprehensive answers with examples


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
- Keep commit messages as one-liners: "[category] brief description"

**Category tags:**
- Check recent git history first - match existing tag patterns when related to current work
- For new features: create descriptive feature tags (e.g. [auth], [search], [ui]) not generic [feat]
- For common changes: use standard tags like [bugfix], [infra], [config], [docs], [tooling]
- Describe the conceptual shape of the work, not just the technical action
