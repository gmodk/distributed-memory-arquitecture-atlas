from __future__ import annotations

"""Educational cryptography/access-structure laboratory shared by all lenses.

The transforms here demonstrate invariants and information/access questions. They
are intentionally *not* presented as a secure encryption construction.
"""

import hashlib
import math
import random
from ..core.finite_field import inv, rank
from ..core.combinatorics import cover_regions
from . import combinatorial, spectral, sheaf


def _rng(key: str, salt: str) -> random.Random:
    material = (key or "atlas-demo-key") + "|" + salt
    seed = int.from_bytes(hashlib.sha256(material.encode("utf-8")).digest(), "big")
    return random.Random(seed)


def _monomial(exp, key: str):
    rng = _rng(key, exp.id)
    perm = list(range(exp.n)); rng.shuffle(perm)
    diag = [rng.randrange(1, exp.p) for _ in range(exp.n)]
    invperm = [0] * exp.n
    for i, old in enumerate(perm): invperm[old] = i
    x = [int(v) % exp.p for v in exp.field_projection]
    z = [(diag[i] * x[perm[i]]) % exp.p for i in range(exp.n)]
    recovered = [0] * exp.n
    for old in range(exp.n):
        i = invperm[old]
        recovered[old] = z[i] * inv(diag[i], exp.p) % exp.p
    return perm, invperm, diag, z, recovered


def _transform_rows(rows, perm, diag, p):
    # z_i = d_i x_{perm[i]}; rewrite every row a*x as b*z.
    dinv = [inv(d, p) for d in diag]
    return [[int(row[perm[i]]) * dinv[i] % p for i in range(len(perm))] for row in rows]


def _keyed_choice(count: int, fraction: float, key: str, salt: str):
    fraction = max(0.0, min(1.0, float(fraction)))
    k = int(round(count * fraction))
    if fraction > 0 and count and k == 0: k = 1
    ids = list(range(count)); _rng(key, salt).shuffle(ids)
    return sorted(ids[:k])


def analyze(exp, approach: str, *, key: str = "", visible_fraction: float = 0.5, q: float = 0.9):
    perm, invperm, diag, blinded, recovered = _monomial(exp, key)
    key_commitment = hashlib.sha256((key or "atlas-demo-key").encode()).hexdigest()[:16]
    matrix, supports = combinatorial.systematic_matrix(exp.n, exp.mode)
    transformed_matrix = _transform_rows(matrix, perm, diag, exp.p)
    original_rank = rank(matrix, exp.p); transformed_rank = rank(transformed_matrix, exp.p)
    generic = {
        "key_commitment": key_commitment,
        "coordinate_permutation_new_to_old": [i+1 for i in perm],
        "nonzero_diagonal_mask": diag,
        "original_field_token": list(exp.field_projection),
        "transformed_field_token": blinded,
        "roundtrip_recovers_original": recovered == [int(v) % exp.p for v in exp.field_projection],
        "full_systematic_rank_before": original_rank,
        "full_systematic_rank_after": transformed_rank,
        "rank_invariant": original_rank == transformed_rank,
    }

    approach = str(approach).lower()
    if approach in {"combinatorial", "probabilistic", "information"}:
        chosen = _keyed_choice(len(matrix), visible_fraction, key, approach + exp.id)
        rows = [matrix[i] for i in chosen]
        r = rank(rows, exp.p) if rows else 0
        access = {
            "visible_regions": [i+1 for i in chosen], "visible_count": len(chosen), "total_regions": len(matrix),
            "observation_rank": r, "full_recovery": r >= exp.n,
            "mutual_information_bits_uniform_source": r * math.log2(exp.p),
            "residual_entropy_bits_uniform_source": (exp.n-r) * math.log2(exp.p),
        }
        if approach == "probabilistic":
            access["erasure_pattern_recovery_invariant_under_monomial_change"] = True
            access["reason"] = "Every surviving row submatrix is right-multiplied by an invertible monomial matrix, so its rank is unchanged."
        interpretation = {
            "combinatorial": "The keyed transform relabels/scales coordinates without changing linear rank. The access subset shows which keyed region family is sufficient for exact systematic recovery.",
            "probabilistic": "Under iid region survival, every erasure pattern has the same rank before and after an invertible coordinate change, so the recovery law is structurally invariant.",
            "information": "Invertible coordinate transforms preserve observation rank, hence preserve mutual information for the uniform finite-field linear source model.",
        }[approach]
        return {"approach": approach, "transform": generic, "access_structure": access, "interpretation": interpretation,
                "security_warning": "This is an invariance/access-structure experiment, not a semantically secure encryption scheme."}

    if approach == "spectral":
        spec = spectral.analyze(exp, preview_limit=100000)
        blocks = spec.get("_active_blocks", [])
        original_rows = [row for b in blocks for row in b["rows"]]
        transformed_rows = _transform_rows(original_rows, perm, diag, exp.p) if original_rows else []
        chosen = _keyed_choice(len(blocks), visible_fraction, key, "spectral" + exp.id)
        kept = [blocks[i] for i in chosen]
        access_rows = [row for b in kept for row in b["rows"]]
        anchor = any(b["kind"] == "anchor" for b in kept)
        r = rank(access_rows, exp.p) if access_rows else 0
        access = {"visible_physical_regions": [blocks[i]["id"] for i in chosen], "anchor_visible": anchor,
                  "constraint_rank": r, "target_rank": max(0, exp.n-1), "projective_recovery": r >= max(0, exp.n-1),
                  "full_recovery_with_anchor": anchor and r >= max(0, exp.n-1)}
        generic.update({"spectral_constraint_rank_before": rank(original_rows, exp.p) if original_rows else 0,
                        "spectral_constraint_rank_after": rank(transformed_rows, exp.p) if transformed_rows else 0})
        return {"approach": approach, "transform": generic, "access_structure": access,
                "interpretation": "This generalizes the original basis-hiding experiment: an invertible coordinate change preserves the rank of the lifted spectral constraint space. The access panel separately tests whether a keyed subset determines the projective token and anchor.",
                "security_warning": "Similarity/basis hiding by itself is not a hardness assumption and is not a secure cryptosystem."}

    if approach == "sheaf":
        regs = cover_regions(exp.n, exp.mode, None)
        relabeled = [tuple(sorted(invperm[i] for i in s)) for s in regs]
        before = sheaf._cohomology(regs, exp.p, min(3, exp.max_dim), "coordinate")
        after = sheaf._cohomology(relabeled, exp.p, min(3, exp.max_dim), "coordinate")
        chosen = _keyed_choice(len(regs), visible_fraction, key, "sheaf" + exp.id)
        selected = [regs[i] for i in chosen]
        covered = sorted({v for s in selected for v in s})
        selected_coh = sheaf._cohomology(selected, exp.p, min(3, exp.max_dim), "coordinate") if selected else {"cohomology_dimensions": []}
        access = {"visible_patches": [i+1 for i in chosen], "covered_coordinates": [i+1 for i in covered],
                  "covers_global_token_coordinates": len(covered) == exp.n, "selected_cohomology_dimensions": selected_coh.get("cohomology_dimensions", [])}
        generic.update({"cohomology_before": before["cohomology_dimensions"], "cohomology_after_relabeling": after["cohomology_dimensions"],
                        "cohomology_invariant": before["cohomology_dimensions"] == after["cohomology_dimensions"]})
        return {"approach": approach, "transform": generic, "access_structure": access,
                "interpretation": "A keyed coordinate relabeling induces an isomorphic cover/nerve, so the sheaf cohomology dimensions are preserved. The access subset asks whether the visible patches cover every global coordinate.",
                "security_warning": "Topological invariance under relabeling is not secrecy; a cryptographic sheaf scheme requires a formal threat model and information-leakage proof."}

    raise KeyError(approach)
