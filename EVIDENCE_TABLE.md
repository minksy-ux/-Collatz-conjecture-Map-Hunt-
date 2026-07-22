# Evidence Table

Use this file to track every important claim with a source and confidence level.

## Status Labels

- proven-theorem: Established by a rigorous published proof.
- computational-evidence: Backed by finite computation only.
- toy-model-observation: True only for maps in this repository.
- open: Not settled.

## Claim Log

| Claim ID | Claim Text | Scope | Status Label | Source (DOI/URL) | Last Checked (YYYY-MM-DD) | Notes |
|---|---|---|---|---|---|---|
| C-001 | Collatz conjecture is open. | Original Collatz map | open | https://doi.org/10.1017/fmp.2022.8 | 2026-07-21 | Keep updated with latest surveys. |
| C-002 | No nontrivial positive cycle is known for Collatz. | Original Collatz map | open | https://doi.org/10.1090/S0025-5718-04-01728-4 | 2026-07-21 | Existing work rules out many cycle classes. |
| C-003 | The map f(x) = -2x^2 + 3x + 1 has escaping integer orbits. | Toy 1D polynomial map in this repo | toy-model-observation | conjecture_search.py output | 2026-07-21 | Example start: -10 exceeds 1e6 in a few steps. |
| C-004 | Counterexamples found by conjecture_search.py do not falsify Collatz. | Interpretation layer | proven-theorem | README scope statement | 2026-07-21 | Keep this distinction explicit in docs. |

## Review Checklist

- Is the claim statement precise and testable?
- Is the scope explicit (Collatz vs toy map)?
- Is the source peer reviewed if the claim is external?
- Is the verification date recent enough?
- Is uncertainty clearly labeled?
