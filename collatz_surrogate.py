"""Build polynomial surrogates that match real Collatz on a finite integer range.

The core idea is interpolation: fit a polynomial P_N so that
P_N(n) = CollatzStep(n) for n = 1..N.

This makes the toy model as "real" as possible on the chosen window while
remaining a single polynomial map.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

from collatz_bridge import collatz_step


@dataclass(frozen=True)
class SurrogateReport:
    train_max_n: int
    degree: int
    train_exact_hits: int
    train_total: int
    holdout_exact_hits: int
    holdout_total: int


def poly_add(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    size = max(len(a), len(b))
    out = [Fraction(0) for _ in range(size)]
    for idx in range(size):
        out[idx] = (a[idx] if idx < len(a) else Fraction(0)) + (b[idx] if idx < len(b) else Fraction(0))
    return trim_poly(out)


def poly_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0) for _ in range(len(a) + len(b) - 1)]
    for i, av in enumerate(a):
        for j, bv in enumerate(b):
            out[i + j] += av * bv
    return trim_poly(out)


def trim_poly(coeffs: list[Fraction]) -> list[Fraction]:
    out = list(coeffs)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def evaluate_poly(coeffs: list[Fraction], x: int) -> Fraction:
    value = Fraction(0)
    power = Fraction(1)
    for coeff in coeffs:
        value += coeff * power
        power *= x
    return value


def lagrange_interpolating_poly(points: list[tuple[int, int]]) -> list[Fraction]:
    """Return polynomial coefficients (ascending power) through integer points."""

    if not points:
        return [Fraction(0)]

    poly = [Fraction(0)]
    for i, (xi, yi) in enumerate(points):
        basis = [Fraction(1)]
        denom = Fraction(1)
        for j, (xj, _) in enumerate(points):
            if i == j:
                continue
            basis = poly_mul(basis, [Fraction(-xj), Fraction(1)])
            denom *= Fraction(xi - xj)
        scaled = [Fraction(yi) * coeff / denom for coeff in basis]
        poly = poly_add(poly, scaled)
    return trim_poly(poly)


def fit_collatz_step_surrogate(max_n: int) -> list[Fraction]:
    if max_n < 1:
        raise ValueError("max_n must be >= 1")
    points = [(n, collatz_step(n)) for n in range(1, max_n + 1)]
    return lagrange_interpolating_poly(points)


def exact_hits(coeffs: list[Fraction], n_values: Iterable[int]) -> tuple[int, int]:
    hits = 0
    total = 0
    for n in n_values:
        total += 1
        predicted = evaluate_poly(coeffs, n)
        target = Fraction(collatz_step(n))
        if predicted == target:
            hits += 1
    return hits, total


def build_report(max_n: int, holdout_end: int) -> SurrogateReport:
    coeffs = fit_collatz_step_surrogate(max_n)
    train_hits, train_total = exact_hits(coeffs, range(1, max_n + 1))
    if holdout_end <= max_n:
        holdout_hits, holdout_total = 0, 0
    else:
        holdout_hits, holdout_total = exact_hits(coeffs, range(max_n + 1, holdout_end + 1))

    return SurrogateReport(
        train_max_n=max_n,
        degree=len(coeffs) - 1,
        train_exact_hits=train_hits,
        train_total=train_total,
        holdout_exact_hits=holdout_hits,
        holdout_total=holdout_total,
    )


def format_poly(coeffs: list[Fraction]) -> str:
    terms: list[str] = []
    for power, coeff in enumerate(coeffs):
        if coeff == 0:
            continue
        if power == 0:
            terms.append(f"({coeff})")
        elif power == 1:
            terms.append(f"({coeff})*x")
        else:
            terms.append(f"({coeff})*x^{power}")
    return " + ".join(terms) if terms else "0"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fit a finite-range polynomial surrogate to the real Collatz step map.")
    parser.add_argument("--train-max-n", type=int, default=12, help="Fit exact Collatz-step values on n=1..train-max-n.")
    parser.add_argument("--holdout-end", type=int, default=20, help="Evaluate exact-hit carryover up to this n.")
    parser.add_argument("--print-poly", action="store_true", help="Print the explicit interpolating polynomial.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    coeffs = fit_collatz_step_surrogate(args.train_max_n)
    report = build_report(args.train_max_n, args.holdout_end)

    print("Finite-range Collatz-step polynomial surrogate")
    print(f"train range: 1..{report.train_max_n}")
    print(f"degree: {report.degree}")
    print(f"train exact hits: {report.train_exact_hits}/{report.train_total}")
    if report.holdout_total > 0:
        print(f"holdout exact hits: {report.holdout_exact_hits}/{report.holdout_total}")
    else:
        print("holdout exact hits: n/a")

    if args.print_poly:
        print("polynomial:")
        print(format_poly(coeffs))


if __name__ == "__main__":
    main()
