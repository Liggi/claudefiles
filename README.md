# Claudefiles 🤖

Version-controlled configuration for Claude Code, inspired by dotfiles.

## What's included

- **Custom hooks** for better git workflow
- **Enhanced statusline** with time, date, model, and directory
- **Settings** for permissions and Claude Code behavior
- **Templates** for project-specific CLAUDE.md files
- **OpenAI CLI** with GPT-5 and web search capabilities

## Quick setup

```bash
git clone <your-repo-url> ~/claudefiles
cd ~/claudefiles
./install
```

The installer will:
- Backup your existing `~/.claude` directory
- Symlink `~/claudefiles/config` → `~/.claude`  
- Make hook scripts executable
- Install OpenAI Python library and setup GPT-5 CLI
- Add claudefiles to your PATH
- Initialize git repo (if needed)

## Structure

```
claudefiles/
├── install              # Setup script
├── gpt5-search          # GPT-5 CLI with web search
├── config/             # Symlinked to ~/.claude
│   ├── settings.json   # Main Claude Code settings
│   ├── settings.local.json  # Local permissions
│   └── hooks/          # Custom hook scripts
└── templates/          # CLAUDE.md templates
```

## Customization

Edit files in `claudefiles/config/` - changes take effect immediately since they're symlinked.

### Hook Scripts

- **git-hook.sh**: Redirects git commands to preferred alternatives (gt, delta)
- **statusline-command.sh**: Custom status bar display

### Adding new projects

Copy `templates/CLAUDE.md.template` to your project root and customize.

### OpenAI CLI Usage

```bash
# Ask GPT-5 with web search
gpt5-search "What's happening in AI today?"

# Direct OpenAI API access  
python3 -m openai api chat.completions.create -m gpt-5 -g user "Hello"
```

**Requirements**: Set `OPENAI_API_KEY` environment variable in your shell config.

## Syncing across machines

```bash
# On new machine
git clone <your-repo-url> ~/claudefiles  
cd ~/claudefiles
./install

# To update
git pull
```

## Troubleshooting

- **Claude Code not recognizing changes**: Restart Claude Code
- **Hooks not working**: Check `chmod +x config/hooks/*.sh`
- **Symlink issues**: Run `./install` again

Your Claude Code setup is now portable and version-controlled! 🎉