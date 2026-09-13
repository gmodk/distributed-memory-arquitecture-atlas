# Validation — Distributed Memory Architecture Atlas 2.0

Date: 2026-09-13

## Automated Python suite

**18/18 tests passed.**

The suite covers:

- random-token reproducibility for all seven semantic token types;
- experiment regeneration and legacy permutation-token import;
- combinatorial full-rank systematic encoding and binary-distance analysis;
- spectral rank-`(n-1)` projective reconstruction and spectral TDA summary;
- probabilistic `q=0` / `q=1` recovery endpoints;
- sheaf gluing compatibility;
- information-theoretic rank/entropy identity;
- cross-approach comparison invariants;
- geometry payloads for all five lenses;
- graph/incidence payloads for all five lenses;
- physical/virtual spectral geometry under rank-basis storage;
- local region inspectors for all five lenses;
- cryptography-lab rank and round-trip invariance for all five lenses;
- sheaf cohomology invariance under keyed coordinate relabeling;
- information-lab mutual-information/rank identity for keyed access subsets.

## Static/runtime validation

Passed:

- Python `compileall` / module compilation;
- JavaScript syntax checks for `app.js`, `graph_lab.js`, and `tda_core.js`;
- Graph/TDA DOM selector coverage: every required graph-lab control ID is present in `index.html`;
- HTTP serving of the application shell and all shared JavaScript assets.

## TDA sanity checks

The shared client-side TDA engine was executed under Node:

- unfilled triangle: `beta_0=1`, `beta_1=1`;
- filled triangle: `beta_0=1`, `beta_1=0`, `beta_2=0`.

## Live HTTP/API smoke tests

For each of the five primary lenses, the running Atlas server successfully served:

- geometry payload;
- graph payload;
- region-detail payload;
- cryptography/access-structure analysis.

The cryptography-lab smoke test additionally verified:

- exact keyed monomial-transform round trip;
- full systematic rank invariance.

## UI feature restoration checklist

Atlas 2.0 contains the following restored/generalized workspaces:

- circular/local geometry exploration;
- paginated selectable region universe;
- region inspector;
- compact incidence graph;
- 2D/3D Graph/TDA laboratory;
- continuous deep zoom and pan;
- 3D orbit controls;
- draggable nodes;
- force, hierarchical, radial, circular, concentric and grid layouts;
- gravity/repulsion/link/damping/collision controls;
- physical-only versus full virtual+physical graph scope;
- ordinary simplicial filtration controls;
- `beta_0` through `beta_3` display;
- persistent Betti curves;
- native Core lab for every mathematical approach;
- Constraints/Diagnostics lab for every approach;
- Cryptography/access-structure lab for every approach.

## Important interpretation boundaries

1. Client-side TDA computes ordinary simplicial homology over `F_2`; it is not sheaf cohomology.
2. Approach-specific filtration values are exploratory ordering functions unless separately backed by an operational theorem.
3. The cryptography lab demonstrates invertible coordinate changes, structural invariants and access diagnostics. It is not a secure encryption or secret-sharing implementation.
4. Graph rendering can be capped for very large virtual universes; this does not change backend mathematical analysis.
