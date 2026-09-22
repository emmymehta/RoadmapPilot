# RoadmapPilot

**An MCP server that lets an AI agent manage a product roadmap through conversation — add features, change priority, move status, and get a summary, all without touching a UI.**

Built on the [Model Context Protocol](https://modelcontextprotocol.io) — the open standard (created by Anthropic, now widely adopted) that lets AI models like Claude call real tools and take real actions instead of just generating text.

## Why this project is a strong portfolio piece

- **Agentic AI** is the single hottest hiring keyword in tech right now, and very few students have shipped an actual MCP server.
- **Directly connects to product management** — you're not just writing code, you're building the exact kind of tool a PM would use to manage a backlog, and demonstrating you understand that workflow.
- **Zero fragile setup** — pure Python, runs anywhere, no Xcode, no App Store, no OS version fights.
- **Genuinely demoable** — at a booth, you can literally have someone watch you type "add a feature called biometric login, high priority" into Claude and see it show up.

## Setup (5-10 minutes)

1. **Make sure you have Python 3.10+.** Check with:
   ```
   python3 --version
   ```

2. **Install dependencies** (from inside the `RoadmapPilot` folder):
   ```
   pip install -r requirements.txt
   ```
   (If `pip` complains, try `pip3` instead, or `pip install -r requirements.txt --break-system-packages`.)

3. **Test the server runs** (optional but reassuring):
   ```
   python3 server.py
   ```
   It should just sit there running — that means it's working. Press `Ctrl+C` to stop it.

4. **Connect it to Claude Desktop.** Open (or create) this file:
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```
   Add this (replace `/full/path/to/RoadmapPilot` with the actual path on your Mac — run `pwd` inside the folder to get it):
   ```json
   {
     "mcpServers": {
       "roadmap-pilot": {
         "command": "python3",
         "args": ["/full/path/to/RoadmapPilot/server.py"]
       }
     }
   }
   ```

5. **Restart Claude Desktop.** You should see a small tools/plug icon indicating RoadmapPilot is connected.

6. **Try it.** In a new chat, ask Claude things like:
   - "What's on my roadmap right now?"
   - "Add a feature called biometric login, mark it high priority"
   - "Move dark mode to in progress"
   - "Give me a summary of the roadmap"

