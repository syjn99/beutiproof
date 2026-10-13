# Agent instructions

## Scope

- This is a design bootstrap, not an implemented Lean analyzer or collector.
- Read [DESIGN](docs/DESIGN.md) before changing behavior or scope.
- Read [data analysis](docs/data-analysis/README.md) before changing collection, storage, or evaluation.
- Default analysis targets a pinned project. File and theorem options only narrow report scope.
- Keep formal verification, measurements, heuristic warnings, and model opinions separate.

## Changes

- Make the smallest change that satisfies the approved task.
- Preserve source provenance, licenses, immutable snapshots, and original human ratings.
- Do not label maintainer code as golden without task-specific human evidence.
- Never execute collected project code on the host or send code to a remote model without permission.
- Keep datasets, credentials, local environments, and generated artifacts out of Git.
- Do not push, open PRs, publish datasets, or expand scope without explicit approval.
- Use repository-local uv and Ruff when Python implementation begins.
- Pin Lean and dependency revisions when Lean implementation begins.

## Writing and checks

- Read [.agents/skills/asd-ste100/SKILL.md](.agents/skills/asd-ste100/SKILL.md) before writing English documentation.
- Preserve uncertainty and safety conditions during rewrites.
- Run the linter without disabled rules or a nonzero baseline on project-authored prose.
- Do not rewrite vendored skill files merely to satisfy their own prose linter.
- Run `python3 .agents/skills/asd-ste100/scripts/ste-lint.py --selftest`.
- Run `python3 .agents/skills/asd-ste100/scripts/ste-lint.py README.md AGENTS.md docs/DESIGN.md docs/data-analysis/*.md --json`.
- Check local links and `git diff --check` before committing.
- Obtain an independent Sol review for each commit. Fix blockers and repeat review before committing.
- Run relevant tests when implementation exists. Documentation lint does not establish analyzer correctness.

## Instruction files

- Keep this document at most 100 lines and concise.
- Keep `CLAUDE.md` as a symbolic link to `AGENTS.md`.
- Keep the shared skill in `.agents/skills/asd-ste100` with its upstream license.
