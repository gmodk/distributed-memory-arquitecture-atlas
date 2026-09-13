# Distributed Memory Architecture Atlas

**Distributed Memory Architecture Atlas** is a single research platform that unifies five previously separate mathematical explorations of distributed memory:

1. **Combinatorial** — region families, contributor hypergraphs, systematic coding and recovery.
2. **Spectral hypergraph** — finite-field polynomial/CRT coordinates, local invariant subspaces and projective reconstruction.
3. **Probabilistic** — random region survival, recovery probabilities, rank distributions and stopping times.
4. **Sheaf-theoretic** — local sections, restrictions, global compatibility and cohomology.
5. **Information-theoretic** — entropy, mutual information, leakage, redundancy, capacity and rate–distortion benchmarks.

The platform's main design rule is **one experiment, many lenses**. A token is created or imported once and remains active when the user moves between approaches.

## Run

No third-party runtime packages are required.

```bash
python app.py
```

Open:

```text
http://127.0.0.1:8000
```

Optional environment variables:

```text
ATLAS_HOST=127.0.0.1
ATLAS_PORT=8000
ATLAS_QUIET=1
ATLAS_DEBUG=1
```

## Shared experiment

An experiment stores:

- semantic token `T`;
- finite-field projection `pi_p(T)`;
- prime field `F_p`;
- M/Q/R architecture mode;
- aggregation rule;
- spectral physical-storage policy;
- random seed;
- region limit used by cover-based computations;
- maximum cohomological/TDA dimension.

Structured token types are preserved as JSON objects. Their finite-field projections are explicit and may be non-injective.

## Random token generator

The shared generator supports:

- characters;
- words;
- integers;
- natural numbers;
- vectors of configurable dimension;
- cyclic permutations of configurable degree;
- polynomial functions of configurable degree.

All generation is reproducible from an integer seed.

## Comparison Lab

The Comparison Lab evaluates the same experiment through all five approaches and exposes bridge invariants. It is intended to reveal structural relationships rather than collapse the approaches into one scalar score.

For example, for a uniform finite-field source observed through the systematic encoding matrix, the combinatorial rank `r` must agree with the information-theoretic identity

`I(T;Y) = r log2(p)`.

## Project layout

```text
distributed-memory-architecture-atlas/
├── app.py
├── src/distributed_memory_atlas/
│   ├── core/
│   │   ├── experiment.py
│   │   ├── token_generator.py
│   │   ├── combinatorics.py
│   │   ├── finite_field.py
│   │   ├── polynomial.py
│   │   └── aggregation.py
│   └── approaches/
│       ├── combinatorial.py
│       ├── spectral.py
│       ├── probabilistic.py
│       ├── sheaf.py
│       ├── information.py
│       └── comparison.py
├── static/
├── docs/
├── examples/
└── tests/
```

The core does not depend on any approach. Approach modules depend on the core and are registered through a common catalog.

## Documentation

- `docs/user-guide/ATLAS_USER_GUIDE.md` — complete application guide.
- `docs/foundations/FOUNDATIONAL_MATHEMATICS.md` — common and approach-specific mathematics.
- `docs/ARCHITECTURE.md` — software architecture and extension rules.
- `docs/MIGRATION_MAP.md` — how functionality from Projects 1–5 maps into the Atlas.
- `VALIDATION.md` — validation results.
- `CHANGELOG.md` — Atlas history.

## Scope and research status

The Atlas is a mathematical research environment, not a production storage engine or proven cryptosystem. The cryptographic ideas investigated in earlier spectral work remain research directions and are not represented as security guarantees here.

---

## Version 2.0 — restored research laboratories

Atlas 2.0 restores the geometry/graph/TDA/security exploration depth of the earlier standalone applications while keeping a single shared experiment and codebase.

Every primary approach now has five workspaces:

- **Geometry** — circular coordinate layout, selectable region universe and local inspector.
- **Graph / TDA lab** — 2D/3D graph, continuous deep zoom, pan/orbit, draggable nodes, multiple layouts, force controls, simplicial filtrations and Betti curves.
- **Core lab** — native mathematics of the lens.
- **Constraints / diagnostics** — detailed algebraic/probabilistic/topological/information diagnostics.
- **Cryptography lab** — educational keyed coordinate-transform and access-structure experiments.

The graph/TDA renderer is implemented once and consumes lens-aware incidence payloads from the Python backend. The mathematical engines remain separate modules.

### Lens-aware exploration

The same region support can be inspected as:

1. a combinatorial contributor set;
2. a spectral local eigenspace constraint;
3. a probabilistic survival block;
4. a sheaf patch/local section;
5. an information observation row.

The **approach-specific TDA filtration** changes with the lens while the ordinary simplicial homology engine remains shared.

### Cryptography lab caveat

The lab uses key-derived invertible monomial transforms over `F_p` and keyed visible-region subsets to study rank, cohomology and information invariants. These experiments are not claimed to provide production encryption or a secure secret-sharing scheme.
