# Handoff System Rules

## File Safety
- Never delete handoff documents without explicit confirmation
- Use versioning when making major changes to documents
- Keep handoff numbering sequential

## Structure Rules
- Place handoff documents directly in the handoffs/ root directory
- Place chat history files only in the 0-system/chat_history directory
- Use the 0-system directory only for system files, not handoffs

## Workflow Guidelines
- Run extraction scripts before attempting to read conversation files
- Verify files moved to milestone directories have been copied correctly
- Always document deviations from original plans

## Chat History Protocol
- NEVER attempt to read files from the chat_history directory
- ALWAYS use shell commands to check if files exist in this directory
- If files exist, IMMEDIATELY run the extraction script
- ONLY work with the extracted files after processing

## Security Enforcement
- Consider the chat_history directory as a RESTRICTED AREA
- Run the CHECK_CHAT_HISTORY function before any handoff creation
- Always validate paths before file operations
- Follow the mandatory protocols defined in the system prompt