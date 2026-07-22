"""Utilities that compare toy polynomial maps against the real Collatz map."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class AlignmentResult:
    start: int
    steps: int
    exact_hits: int
    parity_hits: int
    mse: float


def collatz_step(n: int) -> int:
    """One step of the standard Collatz map on positive integers."""

    if n <= 0:
        raise ValueError("collatz_step is defined for positive integers only")
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1


def collatz_trajectory(start: int, steps: int) -> list[int]:
    """Return [x0, x1, ..., x_steps] under the real Collatz map."""

    if start <= 0:
        raise ValueError("start must be positive")
    if steps < 0:
        raise ValueError("steps must be nonnegative")

    values = [start]
    value = start
    for _ in range(steps):
        value = collatz_step(value)
        values.append(value)
    return values


def polynomial_trajectory(a: int, b: int, c: int, start: int, steps: int) -> list[int]:
    """Return [x0, x1, ..., x_steps] for f(x)=a*x^2+b*x+c."""

    if steps < 0:
        raise ValueError("steps must be nonnegative")

    values = [start]
    value = start
    for _ in range(steps):
        value = a * value * value + b * value + c
        values.append(value)
    return values


def parity_match_count(real_values: list[int], toy_values: list[int]) -> int:
    """Count same-parity points in aligned trajectories."""

    if len(real_values) != len(toy_values):
        raise ValueError("trajectory lengths must match")
    return sum(1 for r, t in zip(real_values, toy_values) if (r % 2) == (t % 2))


def exact_match_count(real_values: list[int], toy_values: list[int]) -> int:
    """Count exactly equal aligned points."""

    if len(real_values) != len(toy_values):
        raise ValueError("trajectory lengths must match")
    return sum(1 for r, t in zip(real_values, toy_values) if r == t)


def mean_squared_error(real_values: list[int], toy_values: list[int]) -> float:
    """Robust mean error over aligned trajectories on a log scale.

    Raw squared error can overflow when toy maps explode. This metric uses
    ``log1p(abs(diff))`` per step, which preserves ordering pressure while
    staying numerically stable for very large integers.
    """

    if len(real_values) != len(toy_values):
        raise ValueError("trajectory lengths must match")
    if not real_values:
        return 0.0

    total = 0.0
    for r, t in zip(real_values, toy_values):
        diff = abs(r - t)
        if diff == 0:
            continue
        # Avoid float conversion overflow for very large integers.
        if diff < (1 << 1022):
            total += math.log1p(float(diff))
        else:
            total += diff.bit_length() * math.log(2.0)
    return total / len(real_values)


def evaluate_alignment(a: int, b: int, c: int, start: int, steps: int) -> AlignmentResult:
    """Compute alignment metrics between real Collatz and a quadratic toy map."""

    real_values = collatz_trajectory(start, steps)
    toy_values = polynomial_trajectory(a, b, c, start, steps)
    return AlignmentResult(
        start=start,
        steps=steps,
        exact_hits=exact_match_count(real_values, toy_values),
        parity_hits=parity_match_count(real_values, toy_values),
        mse=mean_squared_error(real_values, toy_values),
    )
