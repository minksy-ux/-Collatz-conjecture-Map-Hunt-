# Reproducibility Checklist

This runbook standardizes how to report results from this repository.

## Environment

- OS:
- Python version:
- CPU/GPU:
- Date:
- Git commit hash:

## Baseline Validation

Run:

```bash
python -m unittest discover -v .
```

Record:

- Total tests:
- Passed:
- Failed:
- Runtime:

## Core Experiment Commands

Run and capture outputs exactly:

```bash
python conjecture_search.py short_cycle -10 10 --steps 25 --bound 1e6
python conjecture_search.py nonnegative 0 10 --steps 10
python conjecture_search.py bounded_growth -10 10 --steps 10 --bound 100
python conjecture_search.py fast_cycle -10 10 --steps 10
python search_cycles.py --start 5 --steps 12
python period_search.py 2 -10 10
python plot_orbits.py --start 0 --steps 20
```

## Reporting Rules

- Label every result as one of:
  - proven-theorem
  - computational-evidence
  - toy-model-observation
  - open
- State whether the result is about:
  - original Collatz map, or
  - a toy polynomial map in this repository
- Include command, parameter values, and full output snippet.
- Include the commit hash used for the run.

## Regression Protocol

Before publishing any claim update:

1. Run baseline validation tests.
2. Re-run the exact command that produced the claim.
3. Update [EVIDENCE_TABLE.md](EVIDENCE_TABLE.md) with source and date.
4. If a claim changed, explain why in README or release notes.
