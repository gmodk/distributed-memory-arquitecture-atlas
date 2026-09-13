# Mathematical Foundations of the Distributed Memory Architecture Atlas

## 1. Purpose of the unified formalism

The Atlas studies one distributed-memory experiment through five mathematical representations. The goal is not to assert that the five theories are equivalent. Rather, they share a common underlying experiment and ask different questions about it.

The common data are:

- a semantic token `T = (t_1,...,t_n)`;
- an optional finite-field representation `x = pi_p(T) in F_p^n`;
- a graded region geometry M, Q or R;
- a choice of which regions are physically materialized.

The five lenses then study structure, constraints, uncertainty, local-to-global compatibility and information.

---

# Part I — Common foundations

## 2. Tokens

Let `X` be an arbitrary JSON-serializable semantic alphabet. A token is an element

`T in X^n`.

Examples used by the Atlas include scalar integers, natural numbers, characters, words, vectors, permutations and polynomial-function descriptors.

The semantic alphabet is deliberately not assumed to be a field.

## 3. Finite-field projection

Several analyses require linear algebra. For a prime `p`, the Atlas therefore stores an explicit map

`pi_p : X -> F_p`

and applies it coordinatewise:

`x = pi_p(T) in F_p^n`.

For native integer tokens, this can be ordinary reduction modulo `p`. For structured objects the built-in generator uses deterministic projections, for example weighted coordinate sums for vectors or a cyclic-shift exponent for generated cyclic permutations.

These projections need not be injective. Consequently `x` is an **analysis representation**, not an assertion that the semantic object and field vector are equivalent.

This distinction is essential. Algebraic reconstruction of `x` does not automatically imply semantic reconstruction of arbitrary `T` unless `pi_p` is injective on the source family or additional semantic data are retained.

## 4. Prime fields

For prime `p`,

`F_p = Z/pZ`

is a field. Every nonzero element has a multiplicative inverse. Gaussian elimination is therefore exact modulo `p`, giving well-defined notions of matrix rank, nullspace and invertibility.

The Atlas uses dependency-free modular RREF. No floating-point tolerance enters finite-field rank computations.

## 5. M/Q/R graded region families

For `[n] = {1,...,n}`, define

`F_K(n) = {S subseteq [n] : |S| in K}`.

The three standard layer sets are

`M : K = {0,2,4}`,

`Q : K = {0,1,2}`,

`R : K = {0,2,3}`.

Their abstract cardinalities are

`|F_K(n)| = sum_{k in K} C(n,k)`.

Thus

`M(n) = 1 + C(n,2) + C(n,4)`,

`Q(n) = 1 + n + C(n,2)`,

`R(n) = 1 + C(n,2) + C(n,3)`.

The grade-zero element has different semantics in different lenses. In the spectral model it is used as global anchor metadata; in cover-based sheaf computations it is excluded because its support is empty.

---

# Part II — Combinatorial lens

## 6. Systematic distributed memory

The Atlas preserves the systematic V3 interpretation from the combinatorial project.

The first `n` physical regions store the token coordinates directly. Remaining regions use contributor subsets until the declared M/Q/R capacity is reached.

For a field-valued token `x in F_p^n`, every region support `S` determines an incidence row

`a_S in F_p^n`,

where `(a_S)_i = 1` when `i in S` and zero otherwise.

The resulting systematic observation matrix has the form

`A = [ I_n ; B ]`.

Because `I_n` is present,

`rank(A) = n`

over every field.

This gives deterministic recovery from all direct regions and provides additional redundant aggregate observations.

## 7. Kernel/rank criterion

For a linear encoder

`E(x) = A x`,

injectivity is equivalent to

`ker A = {0}`,

which is equivalent to

`rank A = n`.

This is the central deterministic algebraic recovery test in the systematic lens.

## 8. Erasures

If a set of rows is erased and `A_S` denotes the surviving row matrix, then exact linear recovery is possible exactly when

`rank(A_S) = n`.

Thus region erasure is converted into a random or deterministic row-deletion problem.

## 9. Binary code and minimum distance

Over `F_2`, the map

`x -> A x`

defines a binary linear code. Its minimum distance is

`d_min = min_{x != 0} wt(Ax)`.

Then the code detects up to `d_min-1` errors, corrects up to

`floor((d_min-1)/2)`

errors, and tolerates any `d_min-1` erasures.

The Atlas exhaustively computes this invariant only for modest `n`, because enumerating all nonzero messages costs `2^n-1` evaluations.

## 10. Hypergraph viewpoint

Token coordinates are vertices and contributor subsets are hyperedges. Vertex degree measures how many regions depend on a coordinate. This incidence structure is independent of the semantic aggregation used to display region values.

This separation is useful: one may investigate the same contributor geometry with numerical sums, string-like aggregates, vector sums or permutation composition.

---

# Part III — Spectral hypergraph lens

## 11. Polynomial coordinates

Let

`x = (x_0,...,x_{n-1}) in F_p^n`.

Associate the polynomial

`f_x(z) = sum_{j=0}^{n-1} x_j z^j`.

When `p > n`, choose distinct evaluation points

`alpha_i = i`, `i=1,...,n`.

Define

`y_i = f_x(alpha_i)`.

The vector `y` is an evaluation/CRT representation of the same coefficient polynomial. Because the evaluation points are distinct, the Vandermonde map from coefficients to evaluations is invertible.

Equivalently, the linear factors `z-alpha_i` are pairwise coprime and the polynomial CRT gives an isomorphism on the degree-`< n` class.

## 12. Local spectral lines

For a region `S`, restrict the CRT vector:

`y_S = (y_i)_{i in S}`.

The local memory condition is not primarily an aggregate scalar. It is the one-dimensional subspace

`L_S = span(y_S)`.

One convenient operator realizing this line is a rank-one idempotent

`P_S = y_S w_S^T`

with

`w_S^T y_S = 1`.

Then

`P_S y_S = y_S`

and

`ker(P_S-I) = span(y_S)`.

The implementation chooses a pivot coordinate of `y_S` to construct a dual vector `w_S` exactly over `F_p`.

## 13. Lifted constraints

Let `E_S` denote restriction from global CRT coordinates to region `S`. A local condition can be written

`(P_S-I) E_S y = 0`.

Stacking all active region constraints gives

`H y = 0`.

If

`rank H = n-1`,

then

`dim ker H = 1`,

so the surviving constraints determine the projective line `span(y)`.

A scalar anchor fixes scale, after which interpolation recovers the polynomial coefficients `x`.

Thus the characteristic deterministic target of the spectral lens is

`rank H = n-1`,

not `rank H = n`.

## 14. Rank-basis physical storage

The abstract M/Q/R universe can contain many local constraints. The `rank-basis` policy keeps the full universe conceptually but greedily activates only regions that increase the rank of the stacked constraint system until the target `n-1` is reached.

This is a matroid-like independence heuristic over row spaces. It provides a compact physical realization but is not claimed to minimize every possible storage objective globally.

## 15. TDA overlay

Every active nonempty region support may be viewed as a simplex. Closing under faces yields a simplicial complex. Over `F_2`, boundary matrices produce Betti numbers

`beta_k = dim C_k - rank partial_k - rank partial_{k+1}`.

The resulting topology describes the incidence shape of active spectral supports; it is not the same invariant as sheaf cohomology below.

---

# Part IV — Probabilistic lens

## 16. Probability space of region survival

Let the physical regions be indexed by `1,...,N`. A survival state is

`omega in {0,1}^N`.

Under an iid Bernoulli survival model with parameter `q`,

`P(omega) = q^{|omega|}(1-q)^{N-|omega|}`.

Because the sample space is finite, all events are measurable under the power-set sigma algebra.

## 17. Systematic recovery event

For a survival state `omega`, let `A_omega` contain the surviving systematic rows. The recovery event is

`R_sys = {omega : rank(A_omega)=n}`.

The reliability function is

`P_rec(q) = P_q(R_sys)`.

This differs from minimum distance. Minimum distance is a worst-case threshold. `P_rec(q)` weights erasure patterns by a probability law.

Two codes with equal minimum distance can therefore have different reliability curves.

## 18. Spectral recovery event

For the spectral model, let `H_omega` be the stack of surviving active local constraints. Reconstruction additionally requires the global anchor.

The event is

`R_spec = {omega : anchor survives and rank(H_omega)>=n-1}`.

This exposes a tradeoff in rank-basis storage: fewer physical regions reduce storage, but can reduce stochastic redundancy.

## 19. Monte Carlo estimator

For iid trials with recovery indicators `Z_1,...,Z_m`, define

`P_hat = (1/m) sum Z_i`.

Then

`E[P_hat] = P_rec`

and by the law of large numbers `P_hat` converges to `P_rec` as `m` grows.

The Atlas reports a Wilson interval rather than relying on the simplest normal approximation near probabilities close to zero or one.

## 20. Random rank

The surviving rank

`R(omega)=rank(A_omega)`

or

`rank(H_omega)`

is itself a random variable. Its distribution reveals partial information even when full recovery fails.

## 21. Random reveal and stopping time

Reveal regions in random order and let `R_k` be the rank after `k` regions. Define

`tau = inf{k : R_k reaches the recovery target}`.

With the natural filtration generated by the revealed regions, `tau` is a stopping time. Its expected value measures how many randomly encountered regions are typically needed before the memory becomes reconstructible.

---

# Part V — Sheaf-theoretic lens

## 22. Region cover and nerve

Use nonempty memory supports `U_1,...,U_m` as a cover of the coordinate set. The nerve `N(U)` has one vertex per region and a simplex

`{i_0,...,i_k}`

whenever

`U_{i_0} cap ... cap U_{i_k} != empty`.

Thus topology is generated by overlap relations among memory regions rather than directly by token coordinates.

## 23. Coordinate sheaf

To every nerve simplex `sigma`, associate the vector space

`F(sigma) = F_p^{intersection(sigma)}`.

If `sigma` is a face of `tau`, then

`intersection(tau) subseteq intersection(sigma)`,

and the restriction map projects coordinates from the larger support space to the smaller intersection.

This defines a cellular sheaf over the finite nerve.

## 24. Cochains and coboundaries

The degree-`k` cochain group is the direct sum

`C^k = direct_sum_{sigma in N_k} F(sigma)`.

Signed restriction maps define

`delta^k : C^k -> C^{k+1}`.

The compatibility of restrictions implies

`delta^{k+1} delta^k = 0`.

Therefore the cohomology groups are

`H^k = ker(delta^k) / im(delta^{k-1})`.

The Atlas computes their dimensions using exact finite-field ranks:

`dim H^k = dim C^k - rank(delta^k) - rank(delta^{k-1})`.

## 25. Global sections

`H^0` is the space of globally compatible local sections. A concrete global token `x` restricts to local vectors `x|_{U_i}`. On overlaps these restrictions agree identically, so the uncorrupted token-derived sections pass the Atlas compatibility check.

Higher cohomology records obstruction structure associated with the chosen sheaf and overlap geometry.

## 26. Truncation caveat

If the complex is computed only through degree `d`, then `H^d` depends in principle on `delta^d : C^d -> C^{d+1}`. If `C^{d+1}` is omitted, the final reported degree should be treated as provisional.

---

# Part VI — Information-theoretic lens

## 27. Source model

The exact rank-information identity assumes

`T ~ Uniform(F_p^n)`.

Then every source vector has probability `p^{-n}` and

`H(T) = log_2(p^n) = n log_2 p` bits.

## 28. Linear observations

Let

`Y = A T`

with `rank A = r`.

The image of `A` has `p^r` elements. Because a uniform finite-field source maps uniformly onto the image,

`H(Y) = r log_2 p`.

Because `Y` is deterministic given `T`,

`H(Y|T)=0`.

Therefore

`I(T;Y)=H(Y)-H(Y|T)=r log_2 p`.

The kernel has dimension `n-r`, and every observation is consistent with `p^{n-r}` source states. Hence

`H(T|Y)=(n-r) log_2 p`.

This gives the exact decomposition

`H(T) = I(T;Y) + H(T|Y)`.

## 29. Marginal information gain

Adding a region row can increase rank by zero or more. For a scalar systematic row it increases rank by at most one. A rank increment `Delta r` contributes exactly

`Delta I = Delta r log_2 p`

bits under the uniform source model.

The greedy information profile therefore parallels greedy rank-basis selection, although it operates on the systematic observation matrix and optimizes a different object than the spectral constraints.

## 30. Information under erasure

When rows survive randomly, rank becomes random. Because the information formula is linear in rank,

`E[I(T;Y_omega)] = E[rank(A_omega)] log_2 p`.

Likewise

`E[H(T|Y_omega)] = (n-E[rank(A_omega)]) log_2 p`.

Thus the probabilistic and information-theoretic lenses meet exactly through expected random rank under the stated linear source model.

## 31. p-ary symmetric-channel benchmark

For symbol error probability `e`, the classical symmetric `p`-ary channel capacity per source symbol is

`C(e) = log_2 p - H_b(e) - e log_2(p-1)`

for the usual range up to `(p-1)/p`.

This is a benchmark channel model. It is not derived from the Atlas region-failure architecture.

## 32. p-ary Hamming rate–distortion benchmark

For a uniform `p`-ary source under Hamming distortion,

`R(D) = log_2 p - H_b(D) - D log_2(p-1)`

on the nontrivial range, clipped at zero beyond the maximal useful distortion.

Again, this is included as a theoretical reference curve.

---

# Part VII — Bridges among the approaches

## 33. Combinatorial rank and information

For the same systematic matrix `A`, the combinatorial lens computes

`r = rank(A)`.

The information lens converts that same invariant into bits:

`I(T;AT) = r log_2 p`.

The Atlas comparison module explicitly tests that both lenses use the same `r`.

## 34. Rank and probabilistic recovery

The deterministic condition

`rank(A_S)=n`

becomes a random event when `S` is selected by a failure process.

Probability therefore does not replace the combinatorial rank criterion; it puts a measure on the family of rank-sufficient subsets.

The same relation holds for the spectral target `rank(H_S)=n-1` plus anchor survival.

## 35. Spectral constraints and sheaf language

The spectral lens associates local lines or constraint spaces to hyperedges. The sheaf lens asks whether local data on overlapping patches are compatible and what global-section space remains.

A deeper future construction could define a data-dependent spectral sheaf whose stalks are the local spectral lines themselves. The current Atlas keeps the two constructions separate so their invariants remain interpretable.

## 36. TDA and sheaf cohomology

Spectral TDA computes ordinary simplicial homology of active region supports. Sheaf cohomology computes cohomology of data spaces attached to the nerve of a cover.

They may respond to related incidence geometry, but there is no general equality between the displayed Betti numbers and sheaf cohomology dimensions.

## 37. Shared research question

The unified platform makes it possible to ask when different thresholds coincide. Examples include:

- the smallest region family with full systematic rank;
- the smallest spectral family with rank `n-1`;
- the region count at which `H^0` becomes uniquely constrained;
- the point at which conditional entropy becomes zero;
- stochastic thresholds where recovery probability rapidly transitions from near zero to near one.

Discovering structural hypotheses under which these thresholds are related is a research problem, not an assumption built into the software.

---

# Part VIII — Scope

The Atlas is an exploratory mathematical platform. Exact finite-field calculations are exact within the implemented models. Monte Carlo outputs are estimates. Greedy selection is heuristic. Classical channel and rate–distortion curves are benchmarks. Structured-token projections may lose semantic information. No cryptographic security theorem is claimed.

The unifying principle is therefore modest but strong:

> one underlying distributed-memory experiment can support multiple mathematically precise representations, and keeping those representations in one platform makes their agreements, disagreements and bridge invariants directly testable.

---

# 12. Shared geometric, topological and cryptographic exploration layer

Atlas 2.0 adds a common exploratory layer without identifying the five mathematical theories with one another.

## 12.1 Incidence geometry

For a coordinate set `V={1,...,n}` and region family `R`, every approach admits an incidence relation

\[
i\in S,\qquad i\in V,\ S\in\mathcal R.
\]

The browser represents this as a bipartite graph between coordinate nodes and region nodes. The meaning of a region depends on the selected lens:

- combinatorial: contributor subset / systematic observation row;
- spectral: local CRT invariant-subspace constraint;
- probabilistic: random survival block;
- sheaf: cover patch supporting a local section;
- information: observation row whose joint value is quantified through rank.

Thus the shared graph is a common **incidence skeleton**, not a claim of mathematical equivalence.

## 12.2 Simplicial lift and ordinary homology

A nonempty support `S` can be treated as a simplex together with all of its faces. A filtration assigns each region a birth value

\[
\tau(S)\in[0,1].
\]

At threshold `t`, Atlas forms the simplicial complex generated by regions with `tau(S)<=t` and computes boundary ranks over `F_2`. The Betti numbers are

\[
\beta_k(t)=\dim\ker\partial_k(t)-\dim\operatorname{im}\partial_{k+1}(t).
\]

The graph lab can use subset cardinality, region order, physical-first order, or an approach-specific filtration.

This TDA overlay is exploratory. In particular, for the sheaf lens it must be distinguished from sheaf cohomology

\[
H^k(X;\mathcal F),
\]

which depends on stalks and restriction maps, not merely on the underlying simplicial complex.

## 12.3 Lens-specific filtrations

The common topological machinery can be fed different scalar functions without erasing semantic differences.

- **Combinatorial:** support-size/redundancy geometry.
- **Spectral:** physical rank-basis regions enter before virtual constraints.
- **Probabilistic:** a failure-exposure score combines the survival law with structural incidence.
- **Sheaf:** overlap/cover centrality supplies an exploratory patch ordering.
- **Information:** observation/acquisition order supplies an information-oriented filtration.

These functions are visualization/filtration choices unless a separate theorem gives them an operational interpretation.

## 12.4 Invertible keyed coordinate changes

The cryptography lab uses a deterministic key-derived permutation `pi` and nonzero diagonal coefficients `d_i in F_p^*`. Define

\[
z_i=d_i x_{\pi(i)}.
\]

This is an invertible monomial transformation

\[
z=M_Kx,\qquad M_K\in GL_n(\mathbb F_p).
\]

If a linear observation is

\[
y=Ax,
\]

then in the transformed coordinates

\[
y=A M_K^{-1}z.
\]

Therefore

\[
\operatorname{rank}(A M_K^{-1})=\operatorname{rank}(A).
\]

This elementary identity explains several cross-lens invariants in the lab:

1. systematic recoverability is unchanged;
2. every fixed erasure pattern has the same row rank before and after the coordinate change;
3. for the uniform finite-field source, mutual information `r log_2 p` is unchanged;
4. lifted spectral constraint rank is unchanged under the corresponding invertible change of coordinates;
5. coordinate relabeling induces an isomorphic sheaf cover/nerve, so cohomology dimensions are preserved.

These are **invariance statements**, not security theorems.

## 12.5 Access subsets

A key can also deterministically select a subset of regions `A`. Atlas then asks a lens-specific access question.

For linear systematic observations,

\[
\operatorname{rank}(A_A)=n
\]

means exact recovery, while

\[
I(T;Y_A)=\operatorname{rank}(A_A)\log_2 p
\]

quantifies information revealed by the visible rows under the uniform-source model.

For spectral memory, the projective condition is

\[
\operatorname{rank}(H_A)=n-1,
\]

and a scale anchor is additionally required for full recovery.

For the coordinate-sheaf experiment, Atlas records coordinate coverage and the cohomology of the selected patch family. This is a structural access diagnostic, not a complete secret-sharing criterion.

## 12.6 Security limitation

A coordinate permutation, diagonal scaling, similarity transform or basis-hiding operation is efficiently invertible for someone who knows the transform and may leak substantial invariants even when the transform is hidden. Atlas therefore labels the entire workspace an **educational cryptography/access-structure laboratory**. A secure primitive would require a precise adversarial model and a proof or reduction to an accepted hardness assumption.
