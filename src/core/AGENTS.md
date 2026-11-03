# Core Domain Layer Rules (`src/core/AGENTS.md`)

This scoped `AGENTS.md` applies specifically to files inside `src/core/` and demonstrates **hierarchical rule inheritance** (combining with the root `AGENTS.md`).

## Strict Domain Purity Constraints
1. **No Terminal I/O**: Never call `print()` or `input()` inside `src/core/`. Return structured data (`Task`, `dict`, `list`) and let `src/cli.py` format output.
2. **No Process Exit**: Never call `sys.exit()` or import `argparse` inside `src/core/`. Raise domain exceptions (`ValueError`, `KeyError`) instead.
3. **Atomic Reads/Writes**: Always use UTF-8 encoding (`encoding="utf-8"`) when reading or writing JSON files.
