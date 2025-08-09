# Global Claude Instructions

## GPT-5 Web Search Usage
When using the `gpt5-search` command, always:
- Write proper prompts, not search queries
- Always explicitly request web searching in the prompt
- Example: "I need information about X. Please search the web for the latest information and provide a comprehensive answer."
- Remember: You are prompting another LLM that has web search capabilities

## Commit Guidelines
- NEVER add "> Generated with [Claude Code]" or "Co-Authored-By: Claude" to commit messages
- Use clean, standard commit messages without Claude Code attribution
- Use conceptual category tags like [tooling], [config], [docs] etc.
- Keep commit messages as one-liners: "[category] brief description"