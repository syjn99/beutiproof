# Data analysis

## Status

These documents specify a future collection and evaluation pipeline.
No collector, SQLite corpus, or human annotation dataset exists in this scaffold.
Published corpus counts describe source availability, not completed analysis or golden labels.

## Reading order

1. Read [collection](COLLECTION.md) for public-project discovery, snapshots, licensing, and isolation.
2. Read [storage](STORAGE.md) for record identities, persistence, and data boundaries.
3. Read [evaluation](EVALUATION.md) for the development pilot and independent final judgments.

See [DESIGN](../DESIGN.md) for project-wide CLI behavior and proof verification boundaries.

## Three distinct data layers

- **Source corpus:** pinned public project snapshots and automatic analysis outputs.
- **Development pilot:** 60 theorem families used to refine rules and annotation guidance.
- **Final evaluation:** independent finding judgments and proof-comparison pairs with frozen splits.

Source availability does not establish warning precision or human preference.
Maintainer identity supplies provenance, not a positive quality label.
