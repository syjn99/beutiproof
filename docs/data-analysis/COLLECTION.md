# Collection plan

## Status and scope

This document specifies a future collector, not an implemented ingestion service.
Collect public Lean projects as pinned snapshots, preserving project context.
Do not execute repository code during discovery or source inspection.
Maintainer affiliation provides provenance, not a golden quality label.[10]

Source categories include Mathlib, maintainer-associated public projects, educational examples, and reviewed refactoring histories.
Mathematics in Lean supplies educational candidate examples, not automatic golden judgments.[9]

### Layer A: corpus-scale automatic analysis

Inventory all Mathlib Lean source files at a pinned revision.
Attempt analysis of every eligible declaration and module within the frozen supported subset.
Record unsupported cases, failures, timeouts, and exclusions instead of silently dropping them.
Collect declaration findings, import relationships, module structure, and project-level coverage.
A full-corpus report alone does not justify its warnings.

LeanDojo reports 122,517 theorem/proof examples from an earlier Mathlib4 snapshot.[5]
This published count describes source availability, not completed analyzer execution or golden labels.

Before publishing our own exact counts, retain the audit tool revision, invocation, counting rules, input URL, and artifact hashes.
Distinguish lexical source estimates from elaborated declaration counts.
Record exclusions for generated declarations, syntax quotations, comments, and strings.
Refresh counts only through a new explicit snapshot.

### Maintainer-associated public projects

Freeze the official maintainer roster and resolve GitHub identities through public official links.
Kim Morrison, `kim-em`, is an explicit seed for this cohort.[10][12]
The roster defines the cohort, not every public member of the GitHub organization.
Keep former maintainers in a separately labeled optional historical cohort.

Enumerate all public owned repositories for each cohort account with pagination.
Inspect repository trees for Lean files rather than relying only on GitHub's primary-language label.
Also inventory public collaborative projects with documented maintainer involvement.
Document the discovery method and its limits for repositories outside personal accounts.
Never claim to discover every code contribution across GitHub.

For each discovered repository, pin its default-branch commit and record license and toolchain metadata.
Collect eligible Lean files and retain their project context.
Inspect archived projects, forks, tutorials, experiments, and bug reproductions as distinct categories.
Missing redistribution permission permits metadata inventory only, not source redistribution.
Do not access private repositories or collect unrelated personal information.

Deduplicate fork content against its upstream and against Mathlib.
Keep distinct patches and review histories without copying upstream snapshots as independent examples.
Separate repository ownership, maintenance, review, and declaration authorship.
Use public commit and review evidence for attribution, and mark ambiguous attribution as unknown.
File headers and blame alone do not establish sole authorship.

Maintainer status provides provenance, not a positive quality label.
An account can contain excellent libraries, unfinished experiments, and deliberately failing test cases.
Retain poor or disputed cases when relevant instead of selecting only apparent successes.
Cap each author's and project's share of human evaluation to avoid style dominance.
Report those caps and cohort coverage in the frozen manifest.

The collection plan targets complete coverage of the declared public repository inventory.
Report discovered, eligible, collected, excluded, and failed repositories with reasons.
The current design revision does not claim that this maintainer corpus already exists.


## Collection stages

1. Record the official cohort snapshot and public identity evidence.
2. Enumerate repositories with pagination and inspect trees for Lean files.
3. Record discovery status, ownership, license, fork ancestry, and project category.
4. Resolve one immutable commit per selected default branch.
5. Collect eligible sources, Lake files, toolchain declarations, and available dependency lockfiles.
6. Record content hashes and retrieval outcomes in the inventory.
7. Extract project information only inside the required isolation backend.
8. Record successes, partial results, unsupported inputs, and failures without dropping inventory entries.

The snapshot must retain surrounding definitions and imports, not only extracted proof strings.
Submodules and dependencies need separate pinned records and license decisions.
Default-branch snapshots do not claim to cover every branch or historical contribution.

## History and before-and-after pairs

Collect source snapshots first.
Collect Git history and public PR review evidence only where they support attribution or refactoring-pair selection.
Store review rationale separately from inferred quality labels.
A merged PR does not establish improvement on every quality dimension.
Exclude toolchain-only and API-renaming changes from same-environment quality comparisons.

## Safe retrieval and retry policy

Treat archives, filenames, symlinks, configuration, and cached artifacts as untrusted input.
Reject path traversal and archive entries that escape their designated snapshot directory.
Do not follow source symlinks outside the snapshot.
Set download, file-count, archive-expansion, output, and execution limits before ingestion.
Respect API rate limits and retry at most three times for the same failure cause.
Checkpoint each repository result before continuing the batch.

A rate limit, authentication error, license uncertainty, or exhausted resource budget remains an explicit failure or exclusion.
Dependency preparation that executes project code requires isolation even before analysis.
Do not run project-controlled Lake configuration on the host.
See [the design security boundary](../DESIGN.md#8-verification-and-security-boundary).

## Storage handoff

Write discovery and snapshot manifests before extraction starts.
Commit source snapshots to immutable storage without credentials or unrelated personal data.
Record repository counts by discovered, eligible, collected, excluded, and failed status.
Never claim complete collection unless every item in the frozen inventory has a terminal status.
See [storage](STORAGE.md) for record identities and persistence rules.

## Sources

[5] https://leandojo.org/leandojo.html
[9] https://leanprover-community.github.io/mathematics_in_lean
[10] https://leanprover-community.github.io/teams/maintainers.html
[12] https://github.com/kim-em
