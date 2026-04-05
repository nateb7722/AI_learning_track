---
Status: IN PROGRESS
Last updated: 2026-04-05
---

# Learning Track Plan

## Pillar 1: Advanced Statistics & Modeling

### Phase 1 — Multilevel Models & Bayesian Foundation
1. Gelman & Hill: Data Analysis Using Regression and Multilevel/Hierarchical Models
   - Chapter-by-chapter review with visual examples
   - Apply concepts to NFL data and Double Good experimentation
2. Statistical Rethinking (McElreath)
   - Bayesian thinking, DAGs, generative simulation
   - Reinforces and extends G&H with a more Bayesian lens

### Phase 2 — Applied Modeling
3. Apply hierarchical + Bayesian models to:
   - NFL: Bayesian hierarchical models for betting probability distributions
   - Double Good: clustered experiment analysis, semantic knowledge base
4. GAMs (Simon Wood) — flexible non-linear relationships
5. Causal modeling deeper dive — revisit Pearl, Hoover (macro causality)

### Phase 3 — Dynamic & Complex Systems
6. Time series & dynamic models (Kalman filter, Bayesian forecasting)
7. Non-linear dynamics, complex systems (reading TBD)

## Pillar 2: AI & Agent Workflows

### Phase 1 — Claude Code Power User
1. MCP servers, hooks, skills, automation
2. Best practices for context management and prompt engineering
3. Building CLAUDE.md together as we go (learning exercise)

### Phase 2 — First Agent: Fitness & Macro Tracker ← CURRENT
**Project:** Telegram bot for tracking meals/macros and workouts
**Stack:** Python, Telegram, Claude API, SQLite, AWS EC2

Build order (teach concepts before each step):

4. **Database layer** — DONE (2026-04-05)
   - Relational data modeling, normalization, foreign keys
   - SQLite basics, schema design
   - Learned: three-tier workout model (workouts → exercises → sets)

5. **Context windows & prompt engineering** — TAUGHT (2026-04-05)
   - What context windows are, token economics
   - Three approaches: fixed queries vs. two-pass routing vs. tool use
   - Decision: hybrid approach (lightweight system prompt + tool use)

6. **Agent layer (agent.py)** — NEXT
   - Concepts to teach first: tool use / function calling, system prompt
     design, how Claude processes tool calls and results
   - Build: Claude API integration, tool definitions, system prompt builder

7. **Telegram bot (bot.py)**
   - Concepts to teach first: webhooks vs. polling, async Python,
     bot frameworks
   - Build: message handling, routing to agent, response delivery

8. **Onboarding flow**
   - Concepts to teach first: state machines, conversational UX design
   - Build: multi-step onboarding, progressive profile completion

9. **AWS deployment**
   - Concepts to teach first: EC2 basics, security groups, SSH,
     process management, environment variables in production
   - Build: deploy, configure, test end-to-end

10. **Testing & iteration**
    - Use it daily, identify friction, iterate

### Phase 3 — Local Models & Fine-Tuning
11. Running open-source models locally
12. Fine-tuning for specific use cases
13. When and why to fine-tune vs. prompt engineering vs. RAG

## Session Format
- Flexible: Nate picks the focus based on what he feels like that day
- Stats sessions: Nate reads, then we review + build visual examples together
- AI sessions: Teach concepts first, then build together
- Questions welcome anytime, including mid-chapter
- PRIMARY GOAL: learning. SECONDARY GOAL: building.
