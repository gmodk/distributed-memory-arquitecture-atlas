# Software Architecture

## 1. Architectural objective

The Atlas replaces five parallel applications with a modular monolith. The central object is an `Experiment`; mathematical approaches are read-only analytical lenses over that shared object.

The dependency direction is intentionally one-way:

```text
browser shell
    ↓
HTTP API / experiment state
    ↓
approach registry
    ↓
combinatorial | spectral | probabilistic | sheaf | information
    ↓
shared core
```

The core never imports an approach module.

## 2. Canonical experiment

`core.experiment.Experiment` owns the cross-approach state:

- semantic token;
- token type;
- finite-field projection;
- projection rule;
- prime modulus;
- M/Q/R mode;
- aggregation rule;
- spectral policy;
- cover region limit;
- maximum topological/cohomological dimension;
- generator seed and metadata.

An approach may derive additional objects but must not silently mutate the experiment.

## 3. Shared core

### `token_generator.py`
One implementation for all seven token types. The generator always returns the semantic token and the finite-field projection separately.

### `combinatorics.py`
Owns M/Q/R layers, capacities, systematic contributor sequences, pure subset families and cover construction.

### `finite_field.py`
Exact dependency-free arithmetic over prime fields: RREF, rank, nullspace, matrix products, inverses and vector utilities.

### `polynomial.py`
Horner evaluation and CRT/evaluation-coordinate generation.

### `aggregation.py`
Semantic aggregation for the combinatorial lens, including permutation composition.

## 4. Approach contract

Each module exports:

```python
ID = "..."
NAME = "..."
def analyze(experiment, **parameters) -> dict:
    ...
```

`approaches.__init__.REGISTRY` is the only registry the UI/API needs to know.

Adding a future sixth mathematical approach therefore requires:

1. one module;
2. registration in `REGISTRY`;
3. optional specialized UI rendering.

It does not require another server, token generator, finite-field implementation, JSON schema or repository.

## 5. Approach boundaries

The shared core contains primitives, not theory-specific conclusions.

The following remain approach-local:

- minimum distance and coding diagnostics → combinatorial;
- local spectral projector constraints and rank-basis selection → spectral;
- Monte Carlo reliability and stopping times → probabilistic;
- nerves, coboundaries and cohomology → sheaf;
- entropy, mutual information, channel and rate–distortion functions → information theory.

This avoids replacing five duplicated projects with one oversized universal analysis engine.

## 6. Browser architecture

The browser is a single-page vanilla JavaScript shell. It maintains no independent mathematical source of truth.

The browser:

- edits experiment parameters;
- requests token generation;
- imports/exports experiment JSON;
- requests analyses;
- renders returned results.

Python remains the mathematical source of truth.

## 7. API

### Shared state

- `GET /api/catalog`
- `GET /api/experiment`
- `POST /api/experiment`
- `POST /api/experiment/import`
- `POST /api/experiment/reset`
- `POST /api/random-token`

### Analysis

- `GET|POST /api/analyze/combinatorial`
- `GET|POST /api/analyze/spectral`
- `GET|POST /api/analyze/probabilistic`
- `GET|POST /api/analyze/sheaf`
- `GET|POST /api/analyze/information`
- `GET|POST /api/analyze/comparison`

Probability-sensitive endpoints accept `q` and `trials` through POST payloads where relevant.

## 8. State model

Version 1 uses in-process state intentionally. It is a local research application, so there is a single active experiment per running server instance.

A future persistence layer can store a collection of experiments without changing approach APIs. The natural next abstraction is an `ExperimentRepository` with versioned snapshots.

## 9. Research reproducibility

An exported experiment JSON contains all state needed to reconstruct the deterministic architecture, including generator seed and the actual semantic token. Monte Carlo analyses additionally expose their analysis seed in returned results.

## 10. Extension principles

A new mathematical lens should satisfy three conditions:

1. It consumes the canonical experiment or a mathematically explicit derived representation.
2. It does not redefine shared primitives such as M/Q/R or finite-field rank.
3. It documents which outputs are theorems, exact finite calculations, stochastic estimates, heuristics or external benchmarks.

---

# Atlas 2.0 exploratory laboratory layer

Atlas 2.0 adds two shared modules above the common experiment core and below the browser renderer:

```text
Experiment
   |
   +--> five approach engines
   |
   +--> exploration.py  --> geometry / region / graph payloads
   |
   +--> crypto_lab.py   --> keyed invariance / access experiments
```

The exploratory layer does **not** replace approach mathematics. It translates each lens into a common set of inspectable objects:

- coordinate nodes;
- region/hyperedge nodes;
- incidences;
- physical/virtual state;
- an approach-specific filtration score;
- a local region-detail payload.

The browser owns drawing, force layouts, 2D/3D projection and ordinary simplicial TDA. Python remains the source of truth for region semantics, ranks, cohomology, information quantities and keyed transformations.

## Shared graph model

Every lens exports a bipartite incidence graph with coordinate nodes `C_i` and region nodes `R_j`. This common representation is intentionally weak: it records incidence without pretending that contributor regions, spectral constraint blocks, sheaf patches and information observations are mathematically identical.

The graph lab can therefore reuse one renderer while each lens supplies its own semantics and filtration score.

## Ordinary TDA versus sheaf cohomology

The graph/TDA workspace constructs an ordinary simplicial lift from region supports and computes homology over `F_2` client-side. This is distinct from the sheaf approach, whose cohomology is computed from stalks and restriction maps over the selected finite field. Atlas displays both rather than conflating them.

## Cryptography laboratory boundary

`crypto_lab.py` implements invertible monomial coordinate changes and keyed selection of visible region families. These experiments are designed to study invariants, leakage proxies and access conditions. The module is not part of the trusted core and makes no production-security claim.
