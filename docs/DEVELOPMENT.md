# Development scaffold

## Current behavior

The Python package is `beutiproof`, and its console command is `beautiproof`.
Help and version output work after installation.
The parser accepts project roots and reserved file, theorem, format, and provider options.
`check` and `suggest` return exit code 2 with an explicit unavailable-backend message.
They do not check project eligibility, execute target code, invoke providers, or produce findings or patches.

The Lean executable emits a fixed, explicitly labeled scaffold capability response.
It tests compilation and JSON transport shape, not proof analysis.
The Python CLI does not launch this executable yet.
No sandbox, extractor, dataset collector, SQLite schema, or refactoring verifier exists.

## Layout

```text
pyproject.toml               Python package, console entry, test and Ruff settings
uv.lock                      Locked Python development dependencies
.python-version              Python 3.11 development line
src/beutiproof/              CLI module and package entry points
tests/                       CLI regression and Lean build smoke tests
lean/
  lean-toolchain             Pinned Lean 4.34.0 toolchain
  lakefile.toml              Lake library and status executable
  lake-manifest.json         Lean dependency manifest, currently empty
  BeutiProof/Protocol.lean   Explicit scaffold status value
  BeutiProof.lean            Library import root
  Main.lean                  JSON smoke executable
.github/workflows/checks.yml Local-check equivalents for GitHub Actions
```

Data-pipeline architecture remains in [data analysis](data-analysis/README.md).
Future components must follow [DESIGN](DESIGN.md), not infer analysis capability from this scaffold.

## Python setup

Install uv and a supported Python version.
Run commands from the repository root.

```bash
uv sync --locked
uv run beautiproof --help
uv run beautiproof --version
uv run python -m beutiproof --help
```

The project has no Python runtime dependencies.
The development group includes pytest and Ruff.
The lockfile records resolved development dependencies.
Package builds use Hatchling 1.32.4 through an exact backend pin.
Do not install packages into the host Python environment.

## Python checks

```bash
uv run pytest -m "not lean" -q
uv run ruff check src tests
uv run ruff format --check src tests
uv build --out-dir artifacts/dist
```

Build artifacts and local environments stay outside Git.
The source and wheel distributions package the Python CLI scaffold, not a bundled Lean toolchain.

## Lean setup and smoke test

Install Elan and the exact toolchain named in `lean/lean-toolchain`.
The current pin is `leanprover/lean4:v4.34.0`.
No Mathlib dependency exists yet.
Select and pin Mathlib only after the compatibility spike.

From the repository root:

```bash
(cd lean && lake build)
(cd lean && lake exe beutiproof-status)
uv run pytest -q
```

The smoke executable returns this capability declaration, not an analysis result:

```json
{"schema_version":"0.1.0","status":"scaffold","analysis_available":false}
```

The `lean` pytest marker identifies the build integration test.
If Lake is absent, pytest reports that test as skipped.
If Lake exists but its pinned build fails, the test fails instead of hiding the error.
Install the toolchain before running the full suite.
These commands execute only this repository's scaffold, never collected projects.

## Reserved analysis commands

```bash
uv run beautiproof check . --format json
uv run beautiproof suggest . --file Example.lean --theorem demo --provider configured --format json
```

Both commands intentionally exit with code 2.
JSON output contains `status: unsupported`, `stage: scaffold`, and `error.code: not_implemented`.
Text output writes the unavailable-backend message to stderr.
Neither command produces an analysis report or a patch.
Accepted selectors do not imply supported analysis.

## Writing checks

```bash
python3 .agents/skills/asd-ste100/scripts/ste-lint.py --selftest
python3 .agents/skills/asd-ste100/scripts/ste-lint.py README.md AGENTS.md docs/*.md docs/data-analysis/*.md .agents/skills/asd-ste100/UPSTREAM.md --json
```

Do not include untouched upstream examples in the project prose gate.
Preserve upstream provenance and license text.

## CI and next steps

The workflow pins its checkout, uv setup, and Lean action references to commit IDs.
It builds our Lean package and runs Python tests, Ruff, package builds, and writing checks.
A local test run does not establish that hosted CI passed.
Hosted CI needs a separately approved push or pull request.

Implement extraction, isolation, and report contracts in tested increments.
Do not replace unavailable-backend responses with invented measurements.
Do not run collected repository code until its isolation backend exists.
