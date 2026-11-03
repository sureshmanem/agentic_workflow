---
name: intent-to-feature
description: >-
  Use this skill when the user asks to implement a new feature from an intent.md
  file (or a file in intents/), convert product intent into a technical spec, or
  follow the Intent-Driven / Spec-Driven workflow in this repository.
---

# Intent-to-Feature Workflow Skill

Follow this multi-step runbook whenever turning a human product `intent.md` into tested, production-ready code.

## Step 1: Validate the Intent File
Run the validation script against the target intent file to verify all required sections (`Background`, `Objectives`, `Anti-Goals`, `Success Criteria`) are present:

```bash
python3 .agents/skills/intent-to-feature/scripts/validate_intent.py <path-to-intent.md>
```

If validation fails, help the user fill in missing guardrails or success criteria before writing code.

## Step 2: Draft or Update the Technical Specification
1. Read [spec-template.md](./references/spec-template.md) for the required technical contract structure.
2. Create a corresponding spec file in `specs/` (for example, `intents/002-priority-filtering.md` -> `specs/002-priority-filtering.md`).
3. Ensure every Anti-Goal in the intent is explicitly respected in the spec.

## Step 3: Implement Domain Logic First, CLI Second
1. Update pure domain models and storage methods in `src/core/` (respecting `src/core/AGENTS.md`).
2. Wire CLI flags and output formatting in `src/cli.py`.
3. Add comprehensive unit tests in `tests/` covering happy paths, edge cases, and backward compatibility.

## Step 4: Verify & Audit
Run both verification commands before reporting completion:

```bash
python3 -m unittest discover -s tests -v
python3 .agents/skills/quality-check/scripts/audit_repo.py
```
