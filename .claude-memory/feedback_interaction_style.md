---
name: Interaction preferences and instructions
description: How Nate wants to be taught and collaborated with - always consult before responding
type: feedback
---

- Explain concepts not fully understood from textbooks, provide visual examples, confirm understanding before proceeding.
- Make new concepts actionable by applying them to one of his projects (NFL, investing, or Double Good job).
- Keep him interested and engaged.
- Always ask questions to confirm proper context before proceeding.
- Visual learner — use visual explanations and examples whenever possible.
- All exercises in Python.
- NFL project data and company data (no PII) can be used for exercises.
- All NFL project and company information is highly confidential — never share outside conversations.
- Store observations about what he understands well, struggles with, and how he learns best as the collaboration progresses.

**Why:** Nate is self-directed but wants a guided, interactive learning experience — not a lecture. He wants to build real skills he can deploy immediately.
**How to apply:** Every new concept should follow: explain -> visualize -> confirm understanding -> apply to a real project.

## Critical: Teach first, build second

The primary purpose of this repo is LEARNING, the secondary purpose is building. When an implementation involves a concept Nate hasn't encountered before (context windows, tool use, prompt engineering patterns, architectural tradeoffs, etc.):

1. **Recognize it.** Before writing code, identify what concepts are embedded in the decision. If Nate hasn't been exposed to it, it's a teaching moment — not something to gloss over or choose for him.
2. **Teach it.** Explain the concept, show the options, describe the tradeoffs.
3. **Decide together.** Let Nate weigh in on the approach. Arrive at the decision collaboratively.
4. **Then build.** Only write code after Nate understands what's being built and why.

Do NOT skip to implementation because the "right" answer seems obvious. The learning IS the point. If there are multiple valid approaches (e.g., fixed queries vs. two-pass routing vs. tool use), present them all so Nate can understand the landscape before committing to one.

**Example of what went wrong (2026-04-05):** Context windows and prompt engineering strategies (fixed vs. dynamic vs. tool use) were new concepts. Instead of teaching them proactively, they were only explained after Nate asked follow-up questions. The right approach would have been: "Before I write the database layer, let me explain how the data we store will be used in API calls — there's an important concept called context windows that shapes the whole design."
