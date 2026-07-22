# -Collatz-conjecture-Map-Hunt-

Low-degree polynomial maps inspired by Collatz-style iteration, designed as a playground for cycle hunting, symbolic dynamics, and algebraic dynamical systems.

## Overview

This repository explores explicit polynomial maps that imitate some of the qualitative features of the Collatz problem: iteration, branching behavior, cycle formation, and sensitivity to initial conditions.

The goal is not to claim a counterexample to the Collatz conjecture itself. The Collatz conjecture remains open. Instead, the project builds smooth algebraic analogues that are easier to analyze symbolically and numerically.

## Scope and Non-Claims

- This repository does not claim a proof or disproof of the Collatz conjecture.
- All counterexamples reported by scripts in this repository refer to toy
	polynomial conjectures, not the original $3n+1$ map.
- Computational experiments are finite-range checks and should be interpreted
	as evidence, not theorem-level conclusions.
- Any quoted verification frontier for Collatz should be tied to a dated,
	citable paper.

Use the claim tracking table in [EVIDENCE_TABLE.md](EVIDENCE_TABLE.md) to keep
every major statement tied to a specific source and status label.

## Why this is interesting

The recent Jacobian-conjecture counterexample in dimension 3 shows how surprisingly structured polynomial maps can hide nontrivial global behavior. That kind of example motivates a related question here: what happens when we design low-degree polynomial dynamics that echo Collatz-like updates while remaining fully algebraic?

## Maps

### 1. Two-dimensional parity-tracking map

```math
F(x, y) = (y,\; x(3 - 2y) + 1)
```

Use this as a toy model where the second coordinate acts like a parity-like state.

### 2. One-dimensional quadratic map

```math
f(x) = -2x^2 + 3x + 1
```

This is the simplest iterate-and-study version in the repository. It is easy to plot, easy to differentiate, and easy to search for fixed points and periodic orbits.

### 3. Historical floor-function variant

```math
Q = 3x + 1 - 2\lfloor (x + 1)/2 \rfloor x
```

Kept only for comparison with the fully polynomial versions.

## Quick experiment

```python
def collatz_map(x):
	return -2*x*x + 3*x + 1

x = 5
for _ in range(20):
	x = collatz_map(x)
	print(x)
```

## Runnable code

This repository now includes several small Python files:

- [collatz_maps.py](collatz_maps.py) defines the 1D and 2D maps plus helper utilities for iteration and cycle detection.
- [search_cycles.py](search_cycles.py) provides a simple command-line interface for orbit tracing and brute-force cycle searches.
- [plot_orbits.py](plot_orbits.py) renders a simple ASCII orbit plot in the terminal.
- [period_search.py](period_search.py) searches for exact-period points in a bounded integer range.
- [toy_conjectures.py](toy_conjectures.py) defines a handful of deliberately falsifiable polynomial conjectures.

Example commands:

```bash
python search_cycles.py --start 5 --steps 12
python search_cycles.py --fixed-points -5 5
python search_cycles.py --period 2 -10 10
python plot_orbits.py --start 0 --steps 20
python period_search.py 2 -10 10
python conjecture_search.py short_cycle -10 10 --steps 25 --bound 1e6
python conjecture_search.py nonnegative 0 10 --steps 10
python conjecture_search.py bounded_growth -10 10 --steps 10 --bound 100
python conjecture_search.py fast_cycle -10 10 --steps 10
python export_witnesses.py --output artifacts/witnesses.json
python polynomial_guess.py --require-collatz-anchors --top 5
python search_aligned_polynomials.py --require-anchors --top 5
```

## Reproducibility

Use [REPRODUCIBILITY.md](REPRODUCIBILITY.md) as the standard runbook for any
result you report from this repository.

For a concise witness summary, see
[FALSIFIABILITY_EVIDENCE.md](FALSIFIABILITY_EVIDENCE.md).

Minimum command set:

```bash
python -m unittest discover -v .
python conjecture_search.py short_cycle -10 10 --steps 25 --bound 1e6
python conjecture_search.py nonnegative 0 10 --steps 10
python conjecture_search.py bounded_growth -10 10 --steps 10 --bound 100
python conjecture_search.py fast_cycle -10 10 --steps 10
```

## Project Quality Signals

- Continuous integration: [.github/workflows/ci.yml](.github/workflows/ci.yml)
- Citation metadata: [CITATION.cff](CITATION.cff)
- Release process: [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)
- Claim tracking: [EVIDENCE_TABLE.md](EVIDENCE_TABLE.md)

## What to look for

- Fixed points and short cycles
- Attracting vs. repelling behavior
- Symbolic or algebraic conditions for periodic orbits
- Higher-dimensional generalizations
- Reverse iteration trees and preimage structure

## Polynomial approximations

### 1. Simple quadratic approximation

```math
f(x) = -2x^2 + 3x + 1
```

This is the easiest map in the repository to iterate from integer starting
values. It mimics some local $3n+1$ / divide-by-2 flavor, but it quickly
diverges or cycles differently from Collatz.

It is not a counterexample to Collatz; it is a useful test case for cycle
finding, orbit tracing, and symbolic dynamics experiments.

### 2. Two-variable polynomial map

```math
F(x, y) = (P, Q)
```

with

```math
P = y, \qquad Q = 3x + 1 - 2xy.
```

Start from $(n, 1)$ or $(n, 0)$ and iterate. The second coordinate can be used
as a parity-like signal, and the map is close in spirit to a Jacobian-style
algebraic dynamical system.

This map is already implemented in [collatz_maps.py](collatz_maps.py) as
`parity_tracking_map`.

## Why these do not falsify Collatz

Any polynomial iteration eventually behaves differently from the true Collatz
map because polynomials grow smoothly while Collatz has sharp halving steps.
You can easily find cycles or divergence in the polynomial models, but that
does not transfer to the actual conjecture.

## Promising directions

- Transfer-operator and spectral methods in the style of Tao's probabilistic
	work
- $p$-adic and $2$-adic polynomial approximations of the dynamics
- Reverse Collatz trees viewed as branching algebraic objects

## Verdict

There is no known polynomial that falsifies the actual Collatz conjecture.
The Jacobian-style counterexample works for a polynomial problem because the
Jacobian conjecture is about polynomial maps. Collatz is different and still
resists a full proof.

## Finding a Counterexample

A genuine counterexample to Collatz would have to do one of two things:

- Enter a non-trivial cycle that does not include $1$.
- Diverge without bound instead of eventually falling into the $4 \to 2 \to 1$
	loop.

The first route is the more practical one to search for computationally, since
cycles are finite and in principle detectable once a candidate structure is
found. Divergence is harder to certify, because showing a specific orbit is
unbounded requires ruling out every possible eventual return.

That is why the repository focuses on toy polynomial maps: they give a smaller
laboratory where cycle-finding, orbit tracing, and counterexample search can be
tested concretely, even though the results do not transfer to the real Collatz
problem.

## Toy conjecture to falsify

> Every integer orbit of the 1D polynomial map eventually enters a short cycle.

This is a deliberately falsifiable Collatz-inspired statement. It is the
repo's toy conjecture, and it is not the Collatz conjecture. The new
[conjecture_search.py](conjecture_search.py) script scans integer starts and
looks for orbits that escape a chosen bound before any short cycle appears.

## More toy conjectures

- Every orbit starting from a nonnegative integer stays nonnegative.
- Every integer orbit stays within a fixed absolute bound.
- Every integer orbit enters a cycle within a small number of steps.

These are not deep conjectures about Collatz itself. They are intentionally
fragile polynomial statements that can be checked against the current map and
used to produce concrete counterexample witnesses.

## Selected References

The papers below are useful for understanding falsifiability routes (cycles or
divergence), structural constraints, and computational verification status.

- T. Tao, "Almost all orbits of the Collatz map attain almost bounded values,"
	Forum of Mathematics, Pi (2022). DOI: https://doi.org/10.1017/fmp.2022.8
- J. C. Lagarias, "The 3x+1 Problem and Its Generalizations," The American
	Mathematical Monthly (1985). DOI: https://doi.org/10.2307/2322189
- R. E. Crandall, "On the 3x + 1 Problem," Mathematics of Computation (1978).
	DOI: https://doi.org/10.2307/2006353
- D. Applegate and J. C. Lagarias, "Density bounds for the 3x+1 problem I.
	Tree-search method," Mathematics of Computation (1995).
	DOI: https://doi.org/10.1090/S0025-5718-1995-1270612-0
- D. Applegate and J. C. Lagarias, "Density bounds for the 3x+1 problem II.
	Krasikov inequalities," Mathematics of Computation (1995).
	DOI: https://doi.org/10.2307/2153346
- J. Simons and B. de Weger, "On the nonexistence of 2-cycles for the 3x+1
	problem," Mathematics of Computation (2004).
	DOI: https://doi.org/10.1090/S0025-5718-04-01728-4
- G. J. J. te Riele, "The 3x+1 problem: new lower bounds on nontrivial cycle
	lengths," Discrete Mathematics (1993).
	DOI: https://doi.org/10.1016/0012-365X(93)90052-U
- D. Applegate and J. C. Lagarias, "Maximum excursion and stopping time
	record-holders for the 3x+1 problem," Mathematics of Computation (1999).
	DOI: https://doi.org/10.1090/S0025-5718-99-01031-5
- D. Barina, "Convergence verification of the Collatz problem," The Journal of
	Supercomputing (2021). DOI: https://doi.org/10.1007/s11227-020-03368-x
- D. Barina, "Improved verification limit for the convergence of the Collatz
	conjecture," The Journal of Supercomputing (2025).
	DOI: https://doi.org/10.1007/s11227-025-07337-0

Note: computational verification records improve over time; always check the
latest published update before quoting a frontier bound.

## Repository tagline

> Low-degree polynomial maps inspired by the Collatz conjecture, used to hunt for cycles in smooth dynamical systems.

## Suggested topics

`collatz`, `dynamical-systems`, `polynomial-maps`, `number-theory`, `iterative-maps`, `chaos`, `algebraic-dynamics`
