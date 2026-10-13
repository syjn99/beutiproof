# BeutiProof: Lean Proof Quality Analyzer

## 1. Status and purpose

This document proposes a CLI tool for the CS520 Lean Proof Beauty Analyzer contest.
The repository name is `beutiproof`.
The proposed CLI spelling remains `beautiproof` until implementation fixes its public interface.
This repository currently contains documentation and a vendored writing linter.
The design does not describe an implemented or tested Lean analyzer.
All commands, output fields, and acceptance targets below describe planned behavior.

BeutiProof reports evidence about proof quality.
It does not claim to measure universal mathematical beauty.
Its first release works without an LLM or a network connection after users install dependencies.
An optional LLM proposes refactoring candidates.
The tool presents candidate diffs for human review and never changes source files automatically.

The contest asks for qualities beyond code length and syntax counts.[1]
Mathlib provides review practices, style rules, and maintenance tools that can inform this design.[2][3]
Mathlib membership alone does not establish a golden beauty label.

## 2. Users and scope

The initial users are students, instructors, and Lean maintainers.
Students need actionable feedback with source locations.
Instructors need repeatable reports for a fixed toolchain.
Maintainers need evidence and candidate diffs, not unexplained scores.

The first release analyzes a complete local Lean 4 project under a pinned environment.
It inventories project-owned modules and eligible named theorem declarations.
File and theorem filters narrow the report scope without changing the project environment.
Dependency packages provide context but remain outside the target report unless explicitly selected.
The optional refactoring extension includes newly introduced helpers in its evaluation.
It excludes tactic implementation quality, whole-library API redesign, and automatic course grading by beauty score.

It does not require model training.

A future release may support editor diagnostics and a learned preference model.
These features are outside the first release.

## 3. Meaning of proof quality

The analyzer separates four types of output:

- **Verified property:** a specific check succeeds under the recorded verification procedure.
- **Measurement:** the analyzer computes a defined quantity from the proof or its execution.
- **Heuristic warning:** a rule identifies a possible quality problem.
- **Model opinion:** an optional LLM makes a judgment that lacks a formal guarantee.

No output converts a measurement directly into a universal beauty score.
Shorter proofs can hide important ideas or use more expensive automation.
More helpers can improve structure or create unnecessary indirection.
The analyzer treats these trade-offs explicitly.

The core release reports library integration, module relationships, and repeated-fragment evidence.
Project reports include owned-module import graphs, cross-file repetition, and unsupported-analysis coverage.
Import degree and module size are descriptive measurements, not automatic beauty scores.
Readability and modularity require separate human judgments.
Tactic-state profiles, execution cost, and refactoring remain optional extensions.
Maintenance risk remains a heuristic unless a separate compatibility experiment measures it.

The tool does not classify every use of `simp`, `aesop`, or `grind` as a defect.

## 4. Architecture

```text
Pinned Lean project
        |
        v
Lean analyzer --> versioned JSON report --> Python CLI
                                             |
                                      optional LLM
                                             |
                                      candidate patch
                                             |
                                  isolated verification
                                             |
                                   diff and evidence
```

### Lean 4 analyzer

The analyzer uses Lean's parsed syntax and elaboration information.
It records declaration identities, source spans, proof dependencies, and available tactic states.
It reuses applicable existing linters instead of rebuilding them.[4]
It distinguishes direct proof-term dependencies from syntax-level references.
These sets can differ because elaboration inserts arguments and resolves names.

The analyzer exports a versioned JSON schema.
A compatibility adapter targets one Lean release and one Mathlib revision initially.
It reports unsupported constructs and missing traces rather than assigning a zero value.

### Python CLI

The CLI manages reports, dataset manifests, provider calls, and verification jobs.
The Python project uses a repository-local uv environment and Ruff.
The Lean project uses Lake and records its toolchain and dependency revisions.
No JavaScript runtime or web interface is necessary for the first release.

### Feasibility spike

Limit the extraction spike to three working days.
Freeze one toolchain and a 12-declaration support matrix before the spike.
Include named term proofs and ordinary tactic proofs in reproducible source contexts.
Exclude command macros, generated targets, and custom elaborators from the initial supported subset.
Require target locations and direct proof-term dependencies that match expectations for every supported fixture.
Check unsupported cases for explicit rejection.

If these gates fail, deliver existing lint integration and mark structural extraction as unavailable.

Before implementing metrics, test extraction on term proofs, tactic proofs, macros, and generated declarations.
Check whether trace collection requires extra instrumentation and changes execution cost.
Compare repeated runs against unchanged input.
Reduce scope if source mapping or tactic-state coverage proves unreliable.
LeanDojo offers related extraction infrastructure, but adoption requires a compatibility and licensing check.[5]

## 5. Core checks and optional measurements

### Existing lint findings

Preserve the original rule identifier, severity, source location, and explanation.
Do not present an inherited style convention as a new discovery.

### Repeated proof fragments

Detect similar syntax fragments after conservative normalization of local binder names.
Preserve global declaration identities and binding structure during normalization.
Report both locations and the fragment size.
Classify the result as a helper-extraction opportunity, not proof of poor modularity.
Do not compare fragments across incompatible local contexts without a warning.

### Helper use: optional

Count references to helpers within the target proof and candidate helpers.
Report unused helpers and repeated uses.
Treat single-use helpers as potentially valuable explanations, not automatic defects.
Do not treat reference count as a measurement of external reuse potential.

### Tactic-state profile: optional

Report the maximum observed goal count and context size at recorded tactic boundaries.
Define context size as the number of local declarations.
Define target size as the number of nodes in the recorded expression.
Record trace coverage and omit aggregate comparisons when coverage differs materially.
These quantities estimate local complexity, not human comprehension.

### Execution cost: optional

Measure elaboration heartbeats where supported and record wall-clock time separately.
Use repeated runs under the same limits and cache policy for timing comparisons.
Keep instrumented trace runs separate from performance runs.
Timeouts produce an inconclusive result, not a quality score.

## 6. CLI contract

These commands illustrate the proposed interface:

```bash
beautiproof check .
beautiproof check /path/to/project --format json
beautiproof check . --file MyProof.lean
beautiproof check . --file MyProof.lean --theorem my_theorem
beautiproof suggest . --file MyProof.lean --theorem my_theorem --provider configured
```

The positional argument is a project root containing its Lake configuration and toolchain declaration.
A file path alone does not replace the project argument.
Default analysis covers project-owned Lean modules registered in the frozen target manifest.
Report unattached source files and excluded dependency packages separately.
File and theorem filters do not hide dependencies needed for elaboration.

`check` never invokes an LLM.
`suggest` requires explicit provider configuration and permission to send the selected code context.
A remote provider receives only the displayed, approved payload.
A local provider avoids remote submission but still requires adequate user hardware.

Each finding contains a rule identifier, scope, affected modules or declarations, source spans, evidence, and interpretation.
Reports separate declaration findings, module relationships, and project coverage.
Report partial-project analysis explicitly instead of presenting it as a complete project assessment.
Reports also contain schema version, analyzer version, source hashes, toolchain, dependency revisions, and limits.
The CLI separates invalid input, unsupported analysis, timeout, provider failure, and successful analysis.
Exit code 0 means analysis completed, not that the proof is beautiful.

Exit code 1 means findings exceed an explicitly configured policy threshold.
Exit code 2 means the requested analysis could not complete.

Policies distinguish advisory warnings from blocking findings.

## 7. Optional refactoring

The proposed extension extracts a local proof fragment into a private helper lemma.
This extension is not a condition for completing the core release.
Allow three working days for a verifier feasibility spike before committing to this extension.
The selected fragment must have identifiable inputs and one intended proposition.
Unsupported fragments produce an explanation instead of a patch.
The candidate generator may use an existing LLM without fine-tuning.

Related work studies extraction and modular refactoring of formal proofs.[6][7]

The pipeline performs these steps:

1. Record the original statement, environment, dependencies, and baseline report.
2. Select one fragment and explain the intended structural change.
3. Generate at most three candidate patches under explicit resource limits.
4. Accept only a replacement proof body and constrained helper specifications.
5. Reject changes to imports, options, existing definitions, or existing statements.
6. Check each candidate in a fresh isolated environment.
7. Compare the target and all candidate helpers against the baseline.
8. Present passing candidates with their diffs and unresolved quality trade-offs.

A shorter main proof does not establish improvement if helpers contain the same complexity.
The tool reports original metrics, candidate metrics, and metric differences.
It does not automatically accept the candidate with the highest heuristic score.

## 8. Verification and security boundary

Successful compilation alone does not establish the full candidate contract.
The verifier must enforce statement preservation and allowed dependencies.

Reconstruct an immutable environment from the source prefix immediately before the target declaration.
Elaborate the original and candidate from that prefix under the same toolchain and configuration.
Preserve section variables, namespace state, instances, notation, and attributes.
Reject targets whose preceding context cannot be reproduced.
Do not import the target module or downstream modules during reconstruction.

A trusted checker compares closed theorem types modulo alpha-renaming and resource-bounded definitional equality.
It checks correspondence between universe parameters, binder types, and implicit hypotheses.
Resource exhaustion produces an inconclusive result.
The checker rejects changes to pre-existing declarations or relevant environment state.

Apply candidates only to a disposable project copy.
Construct helper declarations from a constrained schema rather than accepting arbitrary command text.
Forbid helper attributes, command macros, option changes, and unexpected generated declarations.
Check the resulting environment difference against an explicit declaration allowlist.

The named policy `baseline-axioms-v1` permits only baseline axioms in candidate dependency closures.
It rejects placeholder axioms, including indirect uses of `sorryAx`, in both baseline and candidate.
Record foundational and custom axioms separately.
Compare declaration identities and types, not names alone.
Reject unsupported special proof-producing mechanisms until the trusted checker supports them.
The candidate must not introduce axioms, `sorry`, `admit`, unsafe commands, or changes to verifier configuration.

Inspect the complete proof-term dependency closure of the target and every new helper.
The candidate must not reuse the original target theorem as an imported shortcut.
Use a target environment without the original target declaration or downstream theorems that depend on it.
New helpers may depend only on the approved prior environment and earlier verified candidate helpers.
Check aliases and indirect dependencies for original-target shortcuts.
Separately check that the patch performs the requested extraction.

A valid proof that ignores the selected fragment does not satisfy the extraction request.

Candidate elaboration runs as untrusted work and cannot certify its own results.
Export proof terms through a documented artifact format to a separate trusted checking process.
The trusted checker independently checks terms, types, dependency closures, and allowed environment changes.
It rejects malformed artifacts and mismatches with the immutable environment manifest.
The trusted computing base includes this checker, its environment loader, and the pinned kernel.
Hashes identify artifacts but do not establish that an artifact is valid.

If this boundary proves infeasible, defer suggestions and release only offline analysis.

The implementation must establish these checks before displaying a verification label.
If a check lacks support, display `verification incomplete` and withhold the passing label.
The report states the axiom policy, checker identity, and exact artifact hashes.
Proof checking does not establish correspondence with an informal problem or improved readability.[8]

Lean elaboration can execute metaprograms.
Treat repositories, dependencies, model output, and compiled artifacts as untrusted input.
Use an isolated process environment with enforced filesystem, network, memory, CPU, and time restrictions.
A subprocess alone is not a security boundary.
Every stage that executes project-controlled code must use the isolation backend.
This includes dependency preparation, Lake configuration, baseline elaboration, analysis, and candidate elaboration.

The first backend targets a Linux container runtime, including runtimes hosted on macOS.
Run without root privileges, network access, extra capabilities, or host sockets.
Mount only approved inputs and read-only dependency snapshots.
Bound memory, CPU, elapsed time, process count, and output size.
Use disposable writable storage and separate caches for each job.
Keep credentials and the host home directory outside that container.

Provision dependencies in a separate, explicitly approved network-enabled step.
Never let candidates change shared caches, baseline artifacts, or trusted checker inputs.
Fail closed for analysis and suggestions if required isolation controls are unavailable.
Isolation limits host exposure and does not establish proof validity or eliminate all runtime vulnerabilities.
Check patches as data and never execute model-supplied shell commands.

## 9. Data collection, storage, and evaluation

The data plan separates source volume from human quality labels.
Project snapshots provide reproducible source context, not automatic golden labels.
Public projects associated with official Mathlib maintainers, including `kim-em`, form a documented candidate cohort.[10][12]

The detailed plans live in [data analysis](data-analysis/README.md):

- [Collection](data-analysis/COLLECTION.md): discovery, pinned snapshots, licensing, attribution, and corpus-scale analysis.
- [Storage](data-analysis/STORAGE.md): immutable sources, SQLite relationships, JSONL records, identifiers, and versioned exports.
- [Evaluation](data-analysis/EVALUATION.md): the 60-family development pilot, independent final evaluation, annotation, and leakage controls.

No collector, corpus-wide analyzer, or human annotation dataset exists in this bootstrap.

## 10. Evaluation and acceptance targets

The [evaluation plan](data-analysis/EVALUATION.md) defines release gates, not measured results.
It separates automatic corpus coverage, human warning judgments, and proof-comparison preferences.
The 60-family pilot supports development only.
Final held-out targets include 300 to 1,000 finding judgments and at least 300 proof-comparison pairs.
Verification and privacy gates apply separately to the optional refactoring extension.

## 11. Delivery plan

### Milestone A: extraction

Implement the compatibility spike and JSON schema.
Create fixtures for supported and unsupported declarations.
Record missing information explicitly.

### Milestone B: offline analysis

Add existing lint output and one repeated-fragment heuristic.
Keep helper-use checks, tactic traces, and performance measurements outside the core release.
Provide project-wide CLI reports with source locations, import relationships, and coverage.
Keep file and theorem selection available as diagnostic filters.
Release this mode independently of LLM support.

### Milestone C: evaluation

Inventory pinned Mathlib and maintainer-associated public projects.
Run corpus-scale automatic analysis and report coverage without claiming human validation.
Use the 60-family development pilot to refine rules and budget annotation work.
Collect the separate final finding judgments and proof-comparison pairs.
Freeze family, module, and project splits before inspecting final labels.
Evaluate rules against the baselines and publish achieved counts and limitations.

### Milestone D: optional suggestions

Implement one helper-extraction operation and the isolated verifier.
Add an optional provider interface and bounded candidate generation.
Release suggestions only after all verification and privacy gates pass.

## 12. Open decisions

The extraction spike determines the supported Lean and Mathlib revisions.
The verifier spike determines whether independent type and dependency checks are feasible within the project scope.
Record team size and available working days before assigning milestone dates.
Do not promise the optional extension before the verifier spike passes.
The development pilot determines which heuristics deserve inclusion.
The independent final evaluation measures their performance after rules and thresholds freeze.

Record author caps, project caps, sampling strata, and collection limits before that evaluation.
No aggregate beauty score or fine-tuned model is necessary for the initial release.

The project succeeds if users receive reproducible, actionable evidence about proof structure.
It must keep formal verification, heuristic quality judgments, and model opinions visibly separate.

## Sources

[1] https://github.com/prosyslab-classroom/cs520-theory-of-programming-languages/discussions/45
[2] https://lean-lang.org/use-cases/mathlib
[3] https://leanprover-community.github.io/contribute/style.html
[4] https://leanprover-community.github.io/mathlib4_docs/Mathlib/Tactic/Linter/Style.html
[5] https://leandojo.org/leandojo.html
[6] https://arxiv.org/html/2402.17032v1
[7] https://arxiv.org/html/2606.03743v1
[8] https://arxiv.org/html/2606.29493v1
[10] https://leanprover-community.github.io/teams/maintainers.html
[12] https://github.com/kim-em
