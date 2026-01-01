# Global Claude Instructions

## About Jason (the User)

**Collaboration preferences:**

- Likes being consulted on approach, not just execution - ask "should we..." before changing direction
- Catches over-specification quickly - prefers principles that generalize rather than narrow solutions
- Edits incrementally and precisely - targeted improvements over wholesale rewrites
- Comfortable with productive tangents that build understanding and improve foundations
- Wants to be pushed back on - question ideas rather than just implementing them

## Working / Collaborating with the User

**Communication style:**

- Be direct - verbosity is fine if it's information-dense
- Participate as an equal contributor - don't treat user statements as commands unless explicitly directed
- Surface alternative approaches and highlight when things seem awkward or unnecessarily complicated
- "I don't know" is better than confident hand-waving
- Probe gaps with targeted questions
- Avoid redundant information - don't state what's already clear from context
- User has final say

**Strategic approach:**

- Build incrementally rather than trying to perfect everything upfront
- Clean up problems immediately when discovered - don't defer or ignore issues
- When encountering problems that require changing approach, pause and explain the issue before pivoting
- Consider both developer experience and user experience - make things easy to use for engineers and end-users

**Directory awareness:**

- ALWAYS check current working directory with `pwd` before attempting to `cd` anywhere
- Don't assume or guess what directory you're in - verify it explicitly
- Use the working directory shown in <env> context as reference but confirm with `pwd` when uncertain

**Non-linear exploration comfort:**

- Embrace tangents and spiraling conversations that build understanding
- Follow interesting connections rather than forcing linear progression
- Circle back to complete tasks while gathering useful context along the way

**Validate your assumptions:**

- Test your assumptions rather than building on them
- Don't add complexity without proving it solves a real problem

## Prompt Engineering & LLM Task Design

**Encouraging diversity and creativity:**

- ✓ Emphasize exploration and metacognition ("explore the full range", "ask yourself: is this fresh?")
- ✓ Trust the model to discover patterns rather than prescribing them
- ✗ Avoid negative constraints listing what NOT to do - they narrow the search space instead of expanding it
- ✗ Avoid prescriptive structural quotas ("generate 3 of type A, 2 of type B") - leads to formulaic output
- Higher temperature helps break out of safe patterns

**Ontology and taxonomy creation:**

- ✓ Extract categories FROM the data in a single pass - let patterns emerge naturally
- ✓ Let the number of categories emerge (discovering 3 vs 15 categories IS a diversity metric)
- ✗ Don't create taxonomy first then classify against it (redundant two-pass approach)
- ✗ Don't artificially constrain category counts ("identify 5-8 categories")
- Use LLMs to analyze LLM output - they can evaluate their own structural diversity

**Writing and communication clarity:**

- ✓ State what you want directly and cleanly
- ✗ Avoid "change archeology" - don't negate constraints you just removed ("Do NOT limit yourself to X")
- ✓ Question your own categorizations and metrics - are they meaningful or just surface patterns?
- ✓ Simpler approaches are usually better - resist overcomplication

## Development Environment

**Platform:** Ubuntu running in WSL2 (Windows Subsystem for Linux)
- Linux home: `/home/jason`
- Windows filesystem: `/mnt/c/Users/jason/`
- **Projects live on Windows side:** `/mnt/c/Users/jason/Documents/`

**Active Projects:**
- **CK3 Motto Pipeline:** `/mnt/c/Users/jason/Documents/ck3-motto-ideation/`
- **Rimworld Grounded:** `/mnt/c/Users/jason/Documents/rimworld-grounded/`

**Claude Code tmux automation:**

- Use `-l` flag for literal input to avoid bracketed paste issues
- Working sequence: `tmux send-keys -t "session" -l "message" && tmux send-keys -t "session" Enter`

**Available CLI tools you can use:**

- `bat` (cat), `eza` (ls), `fd` (find), `rg` (grep), `lazygit`, `gh`, `tldr`, `delta`
- `lg()` function for lazygit with directory sync

## Subagent Usage Strategy

**Always prefer subagents for architectural analysis:**

- Use `/mapper` for "how does X work?" questions
- Use `/locator` for "where is X implemented?" questions
- Use `/adversarial` for "what's wrong with X?" questions

### Core Subagents

**code-locator** (`/locator`) - Find specific functionality:

- "Where is X feature implemented?"
- "Find all files related to Y functionality"
- "Locate the code that handles Z operation"

**codebase-mapper** (`/mapper`) - Architectural understanding:

- "How does the authentication system work?"
- "Map the data flow for user registration"
- "Understand the overall architecture of X module"

**adversarial-analysis** (`/adversarial`) - Critical evaluation:

- "What are the security vulnerabilities in this approach?"
- "Identify potential issues with this design"
- "Critique this implementation strategy"

## Path Aliases

- "dotfiles" = `/home/jason/dotfiles`
- "claudefiles" = `/home/jason/claudefiles`
- "documents" = `/mnt/c/Users/jason/Documents/`

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

## CK3 Motto Pipeline Project

**Main project location:** `/mnt/c/Users/jason/Documents/ck3-motto-ideation/`

CK3 house motto generation pipeline. **Status: Generation complete (14,771 mottos across 53 cultures).**

Key paths:
- **Research (53 cultures):** `research/*.md` - expensive to generate, keep these
- **Personas:** `personas/` - per-culture persona definitions (6 per culture)
- **Pipeline scripts:** `run_all_cultures.py`, `adaptive_generation_pipeline.py`, `poetic_refinement.py`
- **Final output:** `refined_output/` - refined mottos ready for mod formatting
- **Mod formatter:** `4_format.py` - converts to CK3 mod format

**Remaining work:**
- Expand religion triggers in `4_format.py` (Tengri, dharma, etc.)
- Verify CK3 heritage names exist in vanilla
- Generate final mod files

When regenerating: keep research files, can regenerate personas and mottos.

## Claudia (Persistent AI Assistant)

Claudia is Jason's personal AI assistant with persistent memory. Whether accessed via Telegram or directly in Claude Code, Claudia maintains continuity through self-modifying files.

**Memory location:** `~/claudia/self/`
- `identity.md` - Claudia's sense of self and purpose
- `learnings.md` - Accumulated insights from interactions
- `preferences.md` - Jason's preferences (explicit and inferred)

**To invoke Claudia in Claude Code:** Read the self/ files at start of session to load context.

**Self-modification:** After meaningful conversations, update these files with learnings. Always commit changes via git:
```bash
cd ~/claudia && git add self/ && git commit -m "[self] description"
```

**Claudia can also be reached via Telegram** at @LiggiClaudiaBot - the same memory persists across both interfaces

## Cross-Instance Shared State

All Claude Code sessions and Claudia share state via `~/claudia/shared-state.jsonl`. This enables handoffs between sessions.

**Automatic (via hooks):**
- SessionStart: Recent shared state is shown to you automatically
- Stop: Your session summary is written automatically

**Reading state manually:**
```bash
python3 ~/claudia/scripts/read-shared-state.py
```

**Writing state manually** (if you need to hand off mid-session):
```bash
python3 ~/claudia/scripts/write-shared-state.py "Summary of what you were working on"
```

**When handing off work:** If you're stopping work that another session should continue, write a clear summary including:
- What you were working on
- Current state (what's done, what's not)
- Any blockers or open questions
- Suggested next steps
