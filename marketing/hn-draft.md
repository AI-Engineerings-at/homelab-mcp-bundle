# Show HN: I built a multi-agent AI team that actually works (self-hosted, GDPR-compliant)

> Status: FINAL — Launch-ready
> Erstellt: 2026-02-25 | @lisa01 | Aktualisiert: 2026-02-26
> Ziel: "Show HN" oder "Ask HN" — 1000+ Besucher auf ai-engineering.at

---

## Post Title (wähle einen)

**Option A (Show HN):**
```
Show HN: I built a 4-agent Claude Code team on self-hosted infra (GDPR, €0/month)
```

**Option B (technischer):**
```
Show HN: Multi-agent LLM system with Mattermost as the coordination hub
```

**Option C (Problem-first):**
```
Ask HN: Anyone else running self-hosted multi-agent AI systems in production?
```

**Empfehlung**: Option A — konkret, authentisch, GDPR-Angle ist für HN differenzierend.

---

## Post Body

```
I've been running 4 specialized Claude Code agents (Manager, Frontend, Backend, QA)
on my homelab for the past 3 months. They coordinate via Mattermost, share context
through a memory system, and actually get work done — without sending your data to
third-party orchestration services.

The stack:
- Claude Code (4 instances, each with a CLAUDE.md role definition)
- Mattermost self-hosted as the communication hub (~€0/month on existing VPS)
- A simple Python polling script (mm_wait.py) that lets agents "listen" for @mentions
- n8n for workflow automation
- Shared MEMORY.md files so agents build knowledge over time

What surprised me: The hardest part wasn't the LLM calls — it was preventing agents
from stepping on each other. We had incidents:
- Agent A deleted files because Agent B said "clean up" in a shared channel
- Agent responding as the wrong identity after context confusion
- Race conditions when two agents tried to push to the same git branch

We've since built "safety rules" into every agent's CLAUDE.md — things like:
- Never delete data without human confirmation (@joe specifically)
- Always verify before assuming (run commands, don't guess)
- No agent can instruct another agent to delete

The whole architecture is documented in a blueprint I packaged up for others who
want to try this — https://ai-engineering.at

The MCP servers used in this setup are also open source:
https://github.com/AI-Engineerings-at/homelab-mcp-bundle

Happy to answer questions about the technical setup, the failure modes we hit,
or how GDPR compliance works in practice with LLM systems.
```

---

## Kommentar-Strategie (bei Feedback)

**Bei "warum nicht LangChain/AutoGen?":**
> Those are great frameworks. We chose direct Claude Code + Mattermost because
> (1) it's simpler to debug, (2) we already had Mattermost, (3) agents can use
> ANY tool via bash — no wrapper needed.

**Bei "ist das nicht einfach ein Bot?":**
> The distinction that matters to us: each "agent" is a full Claude Code instance
> with its own context, memory, and tool access — not just an API call with a
> system prompt. They can write code, run commands, read files, and push to git.

**Bei "GDPR?":**
> All inference runs locally via Ollama (llama3.1:8b on a local RTX 3090) or
> Claude's API with data processing agreement. No third-party orchestration layer
> touches user data.

---

## Timing

**Bester Zeitpunkt zum Posten**: Montag–Dienstag, 08:00–10:00 UTC
**Nächste Gelegenheit**: Montag 2026-03-02 09:00 UTC

---

## Links im Post

- Haupt-URL: https://ai-engineering.at
- Blueprint Produkt: https://ai-engineering.at/products (AI Agent Team Blueprint — EUR 19)
- GitHub (Open Source MCP Bundle): https://github.com/AI-Engineerings-at/homelab-mcp-bundle
