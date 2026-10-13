# beutiproof

A planned CLI for project-wide Lean proof quality analysis.

This repository contains a Python CLI scaffold, a Lean build scaffold, and design documents.
The `beautiproof` command supports help and version output.
Analysis, collection, and refactoring remain unavailable.

The proposed core works without an LLM after users install its dependencies.
Optional refactoring must preserve the target statement and pass independent checks.
Heuristic quality judgments do not establish mathematical beauty.

## Documentation

- [Design](docs/DESIGN.md): project-wide analysis, proposed CLI, and verification boundaries.
- [Data analysis](docs/data-analysis/README.md): collection, storage, and independent evaluation plans.

See [development](docs/DEVELOPMENT.md) for installation, tests, builds, and current command behavior.
The design describes future analysis behavior, not capabilities implemented by the scaffold.

## Local development

```bash
uv sync --locked
uv run beautiproof --help
uv run beautiproof --version
uv run pytest -q
uv run ruff check src tests
uv run ruff format --check src tests
```

The Lean smoke test requires the pinned toolchain in `lean/lean-toolchain`.
Use `uv run pytest -m "not lean" -q` for Python-only tests.
`check` and `suggest` return exit code 2 because their backends are unavailable.
They do not execute target project code or invoke an LLM.

## Writing checks

The repository includes the ASD-STE100-inspired skill in `.agents/skills/asd-ste100`.
`CLAUDE.md` links to the shared `AGENTS.md` instructions.
The Claude skill path links to the same vendored skill, not a separate copy.

```bash
python3 .agents/skills/asd-ste100/scripts/ste-lint.py --selftest
python3 .agents/skills/asd-ste100/scripts/ste-lint.py README.md AGENTS.md docs/*.md docs/data-analysis/*.md --json
```

These checks cover writing rules, not Lean analyzer correctness or official dictionary compliance.
Upstream skill examples and documentation retain their original text and license.

## License

Project-authored content uses the MIT license.
Third-party material retains its own license and attribution.
