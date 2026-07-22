"""Search Collatz-inspired quadratic polynomials and rank falsifiability strength.

This script explores maps of the form:

    f(x) = a*x^2 + b*x + c

It prioritizes polynomials that quickly produce toy-conjecture counterexamples,
while optionally enforcing Collatz-inspired anchor constraints.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Quadratic:
    a: int
    b: int
    c: int

    def __str__(self) -> str:
        return f"f(x) = {self.a}x^2 + {self.b}x + {self.c}"


@dataclass(frozen=True)
class GuessResult:
    poly: Quadratic
    nonnegative_break_step: int | None
    escape_step: int | None
    escape_start: int | None
    score: int


def iterate(poly: Quadratic, start: int, steps: int) -> list[int]:
    values = [start]
    value = start
    for _ in range(steps):
        value = poly.a * value * value + poly.b * value + poly.c
        values.append(value)
    return values


def first_nonnegative_break(poly: Quadratic, starts: Iterable[int], steps: int) -> int | None:
    for start in starts:
        orbit = iterate(poly, start, steps)
        for idx, value in enumerate(orbit[1:], start=1):
            if value < 0:
                return idx
    return None


def first_escape(poly: Quadratic, starts: Iterable[int], steps: int, bound: int) -> tuple[int, int] | None:
    for start in starts:
        orbit = iterate(poly, start, steps)
        for idx, value in enumerate(orbit[1:], start=1):
            if abs(value) > bound:
                return idx, start
    return None


def score_poly(poly: Quadratic, steps: int, bound: int) -> GuessResult:
    nonnegative_break = first_nonnegative_break(poly, range(0, 11), steps)
    escape = first_escape(poly, range(-10, 11), steps, bound)
    escape_step = escape[0] if escape is not None else None
    escape_start = escape[1] if escape is not None else None

    score = 0
    if nonnegative_break is not None:
        score += 200 - nonnegative_break
    if escape_step is not None:
        score += 200 - escape_step
    if nonnegative_break is not None and escape_step is not None:
        score += 200
    if poly.a < 0:
        score += 20

    return GuessResult(
        poly=poly,
        nonnegative_break_step=nonnegative_break,
        escape_step=escape_step,
        escape_start=escape_start,
        score=score,
    )


def search_best(
    coeff_min: int,
    coeff_max: int,
    steps: int,
    bound: int,
    require_collatz_anchors: bool,
    top_k: int,
) -> list[GuessResult]:
    results: list[GuessResult] = []

    for a in range(coeff_min, coeff_max + 1):
        for b in range(coeff_min, coeff_max + 1):
            for c in range(coeff_min, coeff_max + 1):
                poly = Quadratic(a=a, b=b, c=c)

                if require_collatz_anchors:
                    # Collatz-inspired local anchors: f(0)=1 and f(1)=2.
                    if c != 1:
                        continue
                    if a + b + c != 2:
                        continue

                result = score_poly(poly, steps=steps, bound=bound)
                if result.score > 0:
                    results.append(result)

    results.sort(
        key=lambda r: (
            -r.score,
            r.nonnegative_break_step if r.nonnegative_break_step is not None else 10**9,
            r.escape_step if r.escape_step is not None else 10**9,
        )
    )
    return results[:top_k]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find Collatz-inspired quadratic maps with strong toy falsifiability evidence.")
    parser.add_argument("--coeff-min", type=int, default=-5, help="Minimum coefficient value.")
    parser.add_argument("--coeff-max", type=int, default=5, help="Maximum coefficient value.")
    parser.add_argument("--steps", type=int, default=12, help="Steps used for scoring checks.")
    parser.add_argument("--bound", type=int, default=10**6, help="Escape threshold for |x|.")
    parser.add_argument("--top", type=int, default=5, help="Number of top candidates to print.")
    parser.add_argument(
        "--require-collatz-anchors",
        action="store_true",
        help="Enforce f(0)=1 and f(1)=2.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    top = search_best(
        coeff_min=args.coeff_min,
        coeff_max=args.coeff_max,
        steps=args.steps,
        bound=args.bound,
        require_collatz_anchors=args.require_collatz_anchors,
        top_k=args.top,
    )

    if not top:
        print("No candidates found with positive falsifiability score.")
        return

    print("Top Collatz-inspired toy-falsification candidates:")
    for idx, result in enumerate(top, start=1):
        print(f"{idx}. {result.poly}")
        print(f"   score={result.score}")
        print(f"   nonnegative break step={result.nonnegative_break_step}")
        print(f"   escape step={result.escape_step}, escape start={result.escape_start}")

    best = top[0]
    print("\nBest guess:")
    print(f"  {best.poly}")


if __name__ == "__main__":
    main()