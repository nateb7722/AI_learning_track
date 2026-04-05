---
name: Fitness & Macro Tracker Agent Project
description: First AI agent project - Telegram bot for tracking food macros and workouts, running on AWS with Claude API
type: project
---

Building a Telegram-based fitness tracker as first agent workflow project.

**Stack:** Python, Telegram bot, Claude API (brain), SQLite (storage), Nutrition API, AWS EC2
**Users:** Nate + wife initially, potentially friends/family later
**Interface:** Chat-based via Telegram on phone

**Architecture decisions made:**
- Three-tier workout data model: workouts → exercises → sets (normalized relational design)
- Meals table includes meal_type (breakfast, lunch, dinner, snack, pre/post workout)
- Hybrid context strategy: lightweight system prompt (user profile + daily totals) always included, plus Claude tool use for on-demand data queries
- Tool use / function calling pattern chosen over fixed queries or two-pass routing — Claude decides what data it needs per message

**MVP scope:**
- Telegram bot with multi-user support
- Onboarding flow: asks new users for name, macro/calorie targets, weekly workout goals
- Log meals/snacks via natural language → nutrition lookup → store macros
- Log workouts with exercise and set-level detail via natural language
- Active workout detection (texting sets from the gym)
- Daily summary: intake vs targets
- Weekly summary: workout history vs goals

**Future iterations:** Recipe recommendations, meal timing around workouts, workout planning, fridge inventory, exercise progression tracking

**Completed so far (as of 2026-04-05):**
- database.py — schema and helper functions for all 6 tables (users, meals, workouts, exercises, sets, conversations)
- .env — Telegram bot token stored, Anthropic key placeholder
- Telegram bot created via BotFather (token in .env)
- Cross-device memory sync set up (symlinks on PC and Mac)

**Next up:**
- agent.py — Claude API integration with tool use (teach tool use concept first)
- bot.py — Telegram bot wiring
- Deploy to AWS EC2

**Why this project first:** Low stakes (vs. accountant), daily feedback loops, covers core agent skills (memory, scheduling, context management, tool use). Architecture transfers to other agent projects.

**How to apply:** All code goes in the AI_learning_track repo. Teach concepts before building each component — learning is the primary goal, shipping is secondary.
