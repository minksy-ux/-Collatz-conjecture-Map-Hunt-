# Falsifiability Evidence

This document tracks the strongest current evidence related to falsifiability,
with a strict separation between:

- the original Collatz conjecture, and
- toy polynomial conjectures used in this repository.

## A. Original Collatz Conjecture

Status: open (no known counterexample).

A true falsification would require one of the following:

- a non-trivial positive cycle that never reaches 1, or
- a proven divergent positive orbit.

Current evidence is negative (no such witness known) plus strong partial theory
and large computational verification in the literature listed in README.

## B. Toy Polynomial Conjectures in This Repository

Map used:

```math
f(x) = -2x^2 + 3x + 1
```

These conjectures are intentionally falsifiable and are tested by
[conjecture_search.py](conjecture_search.py).

## Reproducible Command Set

```bash
python conjecture_search.py short_cycle -10 10 --steps 25 --bound 1e6
python conjecture_search.py nonnegative 0 10 --steps 10
python conjecture_search.py bounded_growth -10 10 --steps 10 --bound 100
python conjecture_search.py fast_cycle -10 10 --steps 10
```

## Best Witnesses (Observed 2026-07-21)

| Conjecture Key | Toy Claim | Witness Start | Step | Witness Value | Reason |
|---|---|---:|---:|---:|---|
| short_cycle | Every integer orbit eventually enters a short cycle. | -10 | 3 | -22289521951 | escaped_bound_before_short_cycle |
| nonnegative | Every orbit from a nonnegative integer stays nonnegative. | 0 | 3 | -1 | negative_value_found |
| bounded_growth | Every integer orbit stays within a fixed bound (100 here). | -10 | 1 | -229 | bound_exceeded |
| fast_cycle | Every integer orbit enters a cycle within 10 steps. | -10 | 10 | 1363-digit negative integer | no_cycle_within_step_limit |

For the last witness, the exact step-10 value is available from the script
output and has 1363 decimal digits.

## Interpretation

These are strong falsifiability demonstrations for polynomial toy conjectures,
but they are not evidence of a counterexample to the original Collatz map.
