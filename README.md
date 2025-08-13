# claudefiles ⚙️

Version-controlled configuration and tooling for Claude Code.

## What's included

### Custom Commands (`config/commands/`)
Work seamlessly with the `dev` tmux layout from dotfiles, allowing Claude Code to read and interact with your development panels:
- **/note** - Set contextual notes in your statusline
- **/rightpanel** - Read and act on tmux pane content with custom instructions  
- **/amppanel** - Specialized panel management

### Smart Hooks (`config/hooks/`)
- **File tool enforcement** - Suggests modern alternatives (`bat`, `fd`, `rg`)
- **Comment analyzer** - Blocks redundant code comments using GPT-5-mini
- **Custom statusline** - Rich status display with time, model, directory, and notes

## Installation

```bash
git clone https://github.com/Liggi/claudefiles.git ~/claudefiles
cd ~/claudefiles
./scripts/install
```

The installer handles everything:
- Symlinks `~/claudefiles/config` → `~/.claude`
- Adds `~/claudefiles/bin` to your PATH
- Installs OpenAI Python library for CLI tools
- Makes all scripts executable
- Sets up CLAUDE.md discovery

## Key Features

- **Tmux integration** - Claude Code can read and interact with your development panels via custom commands
- **Smart tooling enforcement** - Hooks suggest modern CLI alternatives and prevent redundant code comments  
- **Contextual statusline** - Rich status display with time, model, directory, and notes for workflow context
- **Behavioral instructions** - CLAUDE.md contains detailed guidelines for how Claude should work in your environment
- **Zero-config setup** - One install script handles everything, no manual configuration needed