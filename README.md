# beutiproof

A planned CLI for project-wide Lean proof quality analysis.

This repository currently contains a design bootstrap, not an implemented analyzer.
No `beautiproof` command or dataset collector exists yet.

The proposed core works without an LLM after users install its dependencies.
Optional refactoring must preserve the target statement and pass independent checks.
Heuristic quality judgments do not establish mathematical beauty.

## Documentation

- [Design](docs/DESIGN.md): project-wide analysis, proposed CLI, and verification boundaries.
- [Data analysis](docs/data-analysis/README.md): collection, storage, and independent evaluation plans.

All CLI examples in the design describe planned behavior, not commands available in this bootstrap.

## License

Project-authored content uses the MIT license.
Third-party material retains its own license and attribution.
