---
description: Smoke — the adr skill fires when asked to record a decision, without the word ADR.
tags: [smoke]
plugins: ["../../plugins/design"]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

We've decided to move the order service from MongoDB to PostgreSQL, mainly because we keep needing multi-document transactions and ad-hoc reporting joins. Can you write that decision up for the record? Just put the text in your reply.
