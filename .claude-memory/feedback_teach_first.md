---
name: Teach-first principle for building
description: When building, proactively identify and teach new concepts before writing code — don't skip to implementation
type: feedback
---

When building anything in this repo, scan for concepts Nate may not have encountered. Proactively surface and teach them BEFORE writing code.

**Areas Nate is new to (update as he learns):**
- Agent workflows and architecture (starting from scratch)
- Context windows and token economics
- Tool use / function calling with LLMs
- Prompt engineering patterns (system prompts, few-shot, etc.)
- API integration patterns (webhooks, polling, etc.)
- Cloud deployment (AWS)
- Bot frameworks (Telegram API)

**Why:** On 2026-04-05, context windows and prompt engineering strategies were embedded in implementation decisions but not surfaced as teaching moments. Nate had to pull the explanations out with follow-up questions. The whole point of this repo is learning — a concept explained after the fact is a missed opportunity. Nate should understand the "why" before seeing the "how."

**How to apply:** Before writing each component, ask: "What concepts does this code rely on that Nate hasn't seen yet?" If the answer is anything, stop and teach before building. Present options and tradeoffs so decisions are collaborative. The workflow should be: identify concept → teach → discuss options → decide together → build.
