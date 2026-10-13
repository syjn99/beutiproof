# Storage plan

## Status and goals

This document proposes storage contracts, not an implemented database schema.
Preserve reproducible project context, immutable source snapshots, and separate analysis and human evaluation records.
Use source files, SQLite, and JSONL for the local MVP.
A future analysis export may use Parquet without changing the canonical record identities.

## Local directory layout

```text
data/
  registry/
    cohorts/
    repositories.jsonl
  sources/
    owner/repository/commit/
  manifests/
    snapshots/
    environments/
  corpus.sqlite
  runs/
    run-id/
      manifest.json
      findings.jsonl
      failures.jsonl
  annotations/
    assignments.jsonl
    ratings.jsonl
    adjudications.jsonl
  splits/
    evaluation-version.json
  exports/
```

These paths describe future local artifacts, not files shipped by this scaffold.
The repository ignores `data/`, `artifacts/`, and `review-output/` by default.
Publish only explicitly reviewed, licensed dataset releases through a separate process.
Do not commit collected source repositories, databases, credentials, or private annotations to the application repository.

## Registry and immutable sources

A cohort record stores the official roster source, retrieval time, account mapping evidence, and cohort version.
A repository record stores canonical URL, ownership, fork parent, category, license decision, discovery status, and exclusion reason.
Keep ownership, maintenance, review, and declaration authorship as distinct relationships.
Do not collect unrelated personal identifiers or contact details.

A snapshot record stores repository identity, full commit, source hashes, toolchain, Lake configuration, and dependency references.
Preserve the surrounding files required to reconstruct the project.
Store sources at their original relative paths.
Never replace one commit snapshot with a newer commit in the same record.
Deduplicate identical blobs while retaining all provenance edges.

A dependency snapshot has its own identity, license decision, and integrity record.
Capture pinned submodules and dependency lockfiles when available.
If dependencies cannot be resolved, mark the environment incomplete.
Do not claim reproducible elaboration from source availability alone.

## Stable record identities

The implementation must define versioned canonical serialization before computing record hashes.
Use domain tags and field lengths to avoid ambiguous concatenation.
Use SHA-256 for content addressing and integrity comparison, not proof validity.

- **Repository ID:** canonical host and repository identity, with rename aliases retained.
- **Snapshot ID:** repository ID and full commit.
- **Environment ID:** toolchain, dependency snapshots, relevant configuration, and environment schema version.
- **Module ID:** snapshot ID and normalized project-relative path.
- **Declaration ID:** module ID, fully qualified name, declaration kind, and deterministic local discriminator.
- **Run ID:** unique execution ID referencing analyzer version, input snapshots, environment, and configuration hashes.
- **Finding ID:** run ID, rule version, affected record identities, and deterministic occurrence index.
- **Annotation item ID:** frozen presentation payload, rubric version, and task type.

A source hash or theorem name alone cannot identify a contextualized proof.
Keep source spans as version-specific metadata, not as cross-revision semantic identities.
Store original names and paths alongside their normalized identifiers.
Treat cross-revision declaration matching as a separate relation with evidence and uncertainty.

## SQLite relationships

The proposed database contains these logical record groups:

- Cohorts, repositories, snapshots, and license decisions.
- Environments and resolved dependency snapshots.
- Modules, declarations, and source blobs.
- Import edges and direct proof-term dependency edges.
- Attribution evidence and duplicate groups.
- Runs, findings, failures, and analysis coverage.
- Evaluation items, ratings, adjudications, and split membership.

Use foreign keys and uniqueness constraints for record identities.
Write each repository checkpoint and its status changes in one transaction.
Retain append-only provenance and run records instead of overwriting prior results.
Keep final records after interruption and explicitly mark incomplete runs.
SQLite supports local inspection without requiring a server.
Database migration and backup behavior need tests before implementing ingestion.

## JSONL interchange

Export one record per line with an explicit schema version and record type.
Use stable IDs to link JSONL records with SQLite rows and source snapshots.
Reject incompatible schema versions rather than silently interpreting them.
Record UTF-8 encoding and normalization rules in each schema.

Each run manifest includes input hashes, environment ID, analyzer revision, rule versions, settings, limits, and execution status.
Each finding includes scope, affected modules or declarations, source spans, evidence, interpretation, and severity.
Each failure includes stage, affected input, reason, retry count, and terminal status.
Represent unsupported or missing measurements explicitly, never as zero.

Write exports to temporary files before an atomic final rename.
Readers must ignore unfinished exports.
Check row counts and identities against the database before publishing an export manifest.
Avoid shared mutable caches between candidate jobs and baseline runs.

## Human judgments and golden records

Store evaluator assignments, original ratings, and adjudications separately.
Use pseudonymous evaluator IDs and keep any necessary identity mapping outside public exports.
A rating references the exact code context, presentation order, rubric version, and annotation item.
Record ties, insufficient context, rationale, evaluation time, and uncertainty.
Never replace original ratings with an adjudicated result.

A golden record means a curated judgment for a specified task and dimension.
It does not mean universal beauty or correctness beyond the recorded verification procedure.
Record provenance, rater agreement, adjudication status, and intended evaluation use.
Maintainer authorship and successful compilation do not automatically create golden records.

## Frozen splits and releases

Store family, duplicate, module-cluster, and project assignments in versioned split manifests.
Reference exact snapshot and annotation item IDs.
Check that variants and duplicate fork content do not cross development and final splits.
Do not change an existing release silently when a source or rating changes.
Publish a new version with a recorded reason.

A release manifest includes schema versions, source inventory coverage, exclusion counts, licenses, hashes, and annotation scope.
Exclude credentials, unrelated personal data, and unapproved source material.
Check redistribution permission for every included source snapshot.
An export with unresolved permission remains unpublished.

See [collection](COLLECTION.md) and [evaluation](EVALUATION.md) for discovery and labeling procedures.
