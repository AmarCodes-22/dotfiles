---
name: tmux
description: Set up a named tmux window in the claude session for this conversation. Routes explicitly-requested commands to the visible terminal.
---

You are setting up a tmux window for this conversation. Follow these steps exactly:

**Step 1 — Check tmux is available**
Run: `which tmux`
If tmux is not installed: tell the user, inform them that all commands will run via the regular Bash tool for this session, and stop here.

**Step 2 — Derive the window name**
Look at the first user message in this conversation. Summarize its intent into a 2–4 word kebab-case slug (skip filler words like "I want to", "can you", "how do I").
Examples:
- "I want to fix the auth bug" → `fix-auth-bug`
- "Run commands in a specific terminal" → `run-in-terminal`
- "Set up a new React project" → `new-react-project`

**Step 3 — Ensure the `claude` session exists**
Run: `tmux has-session -t claude 2>/dev/null || tmux new-session -d -s claude`

**Step 4 — Check for window name collision**
Run: `tmux list-windows -t claude -F '#W'`
If the derived slug already exists in the list: ask the user whether to reuse the existing window or create a new one named `<slug>-2`. Wait for their answer before continuing.

**Step 5 — Create the window (if new)**
Run: `tmux new-window -t claude -n <slug>`

**Step 6 — Confirm setup**
Tell the user: "Tmux window ready: `claude:<slug>`. I'll route commands here when you explicitly ask (e.g. 'run this in my terminal', 'send to tmux'). All other commands run normally."

**Step 7 — Persist this behavior for the rest of the session**
For the remainder of this conversation, follow these rules:

- **Default**: run ALL commands via the regular Bash tool, as normal.
- **Route to tmux only** when the user explicitly asks — phrases like "run this in my terminal", "send to tmux", "run in the foreground", or similar clear intent.
  - Use: `tmux send-keys -t claude:<slug> '<command>' Enter`
- **Check output only** when the user explicitly asks ("what was the output?", "check the terminal", "what did it print?").
  - Use: `tmux capture-pane -t claude:<slug> -p -S -50`
  - Never capture output automatically.
