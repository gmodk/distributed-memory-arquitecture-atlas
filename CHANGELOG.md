# Changelog — Distributed Memory Architecture Atlas

## [2.0.0] — 2026-09-13

### Restored and generalized exploratory laboratories

Version 2.0 rebuilds the unified Atlas after the first consolidation preserved the five mathematical engines but reduced several exploratory capabilities that had existed in the standalone Spectral Hypergraph Memory V5 application.

Every primary mathematical lens now exposes the same five research workspaces:

1. **Geometry** — circular coordinate geometry, selectable region universe, local region inspector and compact incidence view.
2. **Graph / TDA lab** — 2D/3D incidence graph, continuous deep zoom, pan/orbit, draggable nodes, force simulation, six layouts, physics controls, client-side simplicial filtrations, Betti numbers and persistent Betti curves.
3. **Core lab** — native mathematics of the selected lens.
4. **Constraints / diagnostics** — detailed rank, coding, reliability, cohomology or entropy/information diagnostics.
5. **Cryptography lab** — key-derived invertible coordinate transformations and access-structure experiments with explicit security caveats.

### Added

- Shared `approaches/exploration.py` for lens-aware geometry, region inspection and graph payloads.
- Shared `approaches/crypto_lab.py` for educational keyed invariance/access experiments.
- Geometry semantics for all five lenses:
  - combinatorial contributor regions;
  - spectral CRT/eigenspace regions;
  - probabilistic survival blocks;
  - sheaf patches/local sections;
  - information observation rows.
- Approach-specific graph filtration scores.
- Ordinary simplicial TDA overlay available from all five approaches.
- Explicit distinction between ordinary simplicial homology and sheaf cohomology.
- Keyed monomial coordinate transforms over `F_p` with exact round-trip validation.
- Cross-lens rank-invariance experiments under invertible coordinate changes.
- Access-subset experiments:
  - rank/recovery and information leakage for combinatorial/information lenses;
  - erasure-pattern invariance for probability;
  - projective rank + anchor access for spectral memory;
  - patch coverage and cohomology invariance for sheaves.
- Graph rendering cap/warning for very large virtual region universes.
- Additional theorem/regression tests for geometry, graph payloads and cryptography-lab invariants.

### Changed

- Atlas server/version advanced to 2.0.
- The former single results dashboard is now a multi-workspace research UI.
- Spectral Hypergraph functionality is no longer a reduced summary: CRT geometry, physical/virtual regions, graph/TDA, constraint-rank diagnostics and security experiments are again directly explorable.
- Graph/TDA infrastructure is implemented once and reused by all lenses.

### Security note

The cryptography workspace is an educational research laboratory. Key-derived coordinate changes, relabeling, similarity/basis-hiding phenomena and access-structure tests are **not** claimed to constitute a secure encryption or secret-sharing construction without a formal threat model and reduction.

---

## [1.0.0] — 2026-09-13

### Added

- Initial unified Atlas project.
- One persistent experiment shared by five mathematical approaches.
- Shared token generator, finite-field primitives, M/Q/R combinatorics and JSON import/export.
- Combinatorial, spectral, probabilistic, sheaf and information-theoretic analysis modules.
- Cross-approach Comparison Lab.
- Migration compatibility with legacy permutation-token JSON examples.

### Limitation addressed by 2.0

The initial consolidation intentionally emphasized shared engines and cross-approach state, but it compressed the richer geometry, graph, TDA and cryptography workspaces of the earlier standalone applications into summary panels. Version 2.0 corrects that regression.
