# Claudefiles 🤖

Version-controlled configuration for Claude Code, inspired by dotfiles.

## What's included

- **Custom hooks** for better git workflow
- **Enhanced statusline** with time, date, model, and directory
- **Settings** for permissions and Claude Code behavior
- **Templates** for project-specific CLAUDE.md files

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
- Initialize git repo (if needed)

## Structure

```
claudefiles/
├── install              # Setup script
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