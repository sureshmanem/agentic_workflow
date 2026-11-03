# Agentic Workflow Lab — TaskPulse

A hands-on learning repository demonstrating how modern AI coding agents use **`intent.md`**, **`AGENTS.md`**, **`SKILL.md`**, **Subagent `.md` files**, and **Lifecycle Hooks** together on a real, working Python project (**TaskPulse**).

---

## Repository Map: Every Agentic File Explained

```text
agentic_workflow/
├── intent.md                                      # 1. PRODUCT INTENT ("Why & What" + Anti-Goals)
├── intents/
│   └── 002-priority-filtering.md                  #    Ready-to-build feature intent for practice!
├── specs/
│   └── 001-core-task-tracker.md                   # 2. TECHNICAL SPEC ("How" — contract from intent)
├── AGENTS.md                                      # 3. GLOBAL REPO RULES (Always-on operating manual)
├── .agents/                                       # 4. WORKSPACE CUSTOMIZATIONS (Auto-discovered)
│   ├── skills/                                    #    Progressive-disclosure procedural runbooks
│   │   ├── intent-to-feature/
│   │   │   ├── SKILL.md                           #    Teaches agent how to ship an intent end-to-end
│   │   │   ├── references/spec-template.md        #    Loaded ONLY on-demand when drafting a spec
│   │   │   └── scripts/validate_intent.py         #    Executable helper script for the agent
│   │   └── quality-check/
│   │       ├── SKILL.md                           #    Teaches agent how to audit repo health
│   │       └── scripts/audit_repo.py              #    AST check verifying src/core/AGENTS.md purity
│   ├── agents/                                    #    Custom Subagent Personas (isolated context)
│   │   ├── code-reviewer.md                       #    Read-only code review specialist
│   │   └── spec-architect.md                      #    Intent -> Spec planning specialist
│   └── hooks.json                                 #    Lifecycle hooks (e.g., PostToolUse checks)
├── src/
│   ├── cli.py                                     # Presentation layer (argparse CLI)
│   └── core/
│       ├── AGENTS.md                              # 5. SCOPED HIERARCHICAL RULE (pure domain only!)
│       ├── models.py                              # Task dataclass & validation
│       └── store.py                               # JSON persistence engine
└── tests/                                         # Unit & CLI integration tests
```

---

## Quick Start (Zero Dependencies — Python 3.9+ Stdlib)

```bash
# 1. Run unit tests
python3 -m unittest discover -s tests -v

# 2. Run the architecture & SKILL.md / AGENTS.md audit script
python3 .agents/skills/quality-check/scripts/audit_repo.py

# 3. Validate an intent file
python3 .agents/skills/intent-to-feature/scripts/validate_intent.py intents/002-priority-filtering.md

# 4. Try the TaskPulse CLI
python3 -m src.cli add "Master SKILL.md and AGENTS.md" --priority high
python3 -m src.cli list
python3 -m src.cli done 1
python3 -m src.cli stats
```

---

## 4 Hands-On Prompts to Try With Your Agent

1. **Test `SKILL.md` + `intent.md` End-to-End**:
   > *"Implement `intents/002-priority-filtering.md` using the `intent-to-feature` skill."*
2. **Test Hierarchical `AGENTS.md` Guardrails**:
   > *"Run a `quality-check` on this repository and verify `src/core/` follows its local `AGENTS.md`."*
3. **Test Subagent Delegation (`.agents/agents/`)**:
   > *"Delegate a review of `src/` and `tests/` to a code-reviewer subagent following `.agents/agents/code-reviewer.md`."*
4. **Author a New Skill**:
   > *"Create a new skill `.agents/skills/release-notes/SKILL.md` that summarizes completed tasks and recent git commits into `CHANGELOG.md`."*
