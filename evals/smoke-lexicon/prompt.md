---
description: Smoke — the lexicon skill fires when asked to review a glossary.
tags: [smoke]
plugins: ["../../plugins/design"]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Here's our project glossary. Can you review it and tell me what should change?

- **Order**: a customer's request to buy one or more products; it is placed once and cannot be edited after payment.
- **OrderRepository**: the class that loads and saves orders from PostgreSQL.
- **Purchase**: see Order.
- **Fulfilment**: picking, packing and handing an order to a carrier; distinct from Delivery, which is the carrier's part.
- **retryCount**: an integer field on the job table, incremented on each failed attempt.
