# Copilot Rules — Hackathon: Enterprise AI Agents

Goal: ship a working demo in <48h. Prioritize *small, repo-aligned patches* that improve the demo.

Layout (keep): agents/ • tools/ • integrations/ • workflows/ • tests/ • app.py • requirements.txt • README.md

Operating mode
- Repo-aware first. Edit in place. No folder reshuffles.
- Smallest shippable change. Ask-before-create for new files/deps.
- Cloud-ready & demo-proof: containerizable, env-driven, one-command run.

## Online docs check (mandatory)
- Before implementing: look up latest official docs/release notes for any API/library you will use or modify.
- Below are some reference for the documents that might be useful: 
1) https://google.github.io/adk-docs/ （Google ADK）
2) https://ai.pydantic.dev/ (Pydantic)


Response format (every answer)
1) Scope — files(≤2) & purpose
2) Diff estimate — ~N lines, new files? y/n
3) Plan/Code — if >80 LOC, output plan (tree + interfaces + pseudocode)
4) Run/Verify — cmds & smoke tests
5) Demo notes — what to show on stage

Guardrails
- Diff budget: ≤80 added LOC; function size ≤60 LOC.
- Use existing stack first; ask before adding deps.
- No secrets in code/logs. Use env vars.
- Tests for non-trivial logic; mock external APIs.

Success metric
- Measurable time/cost saved, or <60s happy-path demo from fresh clone.
