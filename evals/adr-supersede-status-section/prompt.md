---
description: "Superseding an ADR whose status is a ## Status section: the old one is marked in that field and otherwise untouched, the new one names it, the index follows."
tags: [adr]
plugins: ["../../plugins/design"]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

ADR-0002 no longer holds. The replacement gauges went in last week and they push each reading over MQTT as it is taken, so we're subscribing instead of polling; the old HTTP endpoints are gone with the old gauges. Readings now reach the pilots within seconds rather than minutes.

Please record that. Use exactly this title: Subscribe to gauge readings over MQTT instead of polling
