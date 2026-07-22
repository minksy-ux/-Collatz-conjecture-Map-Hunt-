"""Collatz-inspired polynomial maps and small utilities for iteration and cycle search.

The module is dependency-free so it can be used from a plain Python shell or
imported into notebooks, scripts, or symbolic workflows.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, List, Sequence, Tuple

Number = complex | float | int
Vector2 = Tuple[Number, Number]


def one_dimensional_map(x: Number) -> Number:
    """The basic 1D polynomial toy map used in the README."""

    return -2 * x * x + 3 * x + 1


def parity_tracking_map(x: Number, y: Number) -> Vector2:
    """A simple 2D Collatz-inspired map.

    The second coordinate acts like a state variable that can be used to build
    more structured experiments.
    """

    return y, x * (3 - 2 * y) + 1


def iterate_map(func: Callable[[Number], Number], start: Number, steps: int) -> List[Number]:
    """Return the orbit of a 1D map starting at `start` for `steps` iterations."""

    orbit = [start]
    value = start
    for _ in range(steps):
        value = func(value)
        orbit.append(value)
    return orbit


def iterate_vector_map(
    func: Callable[[Number, Number], Vector2],
    start: Vector2,
    steps: int,
) -> List[Vector2]:
    """Return the orbit of a 2D map starting at `start` for `steps` iterations."""

    orbit = [start]
    x, y = start
    for _ in range(steps):
        x, y = func(x, y)
        orbit.append((x, y))
    return orbit


def detect_cycle(orbit: Sequence[Number], tolerance: float = 1e-12) -> Tuple[int, int] | None:
    """Detect a repeated value in a 1D orbit.

    Returns (mu, lam) where mu is the index at which the cycle begins and lam
    is the cycle length. Returns None if no cycle is found.
    """

    for start_index in range(len(orbit)):
        for cycle_length in range(1, (len(orbit) - start_index) // 2 + 1):
            repeated = True
            for offset in range(cycle_length):
                left = orbit[start_index + offset]
                right = orbit[start_index + offset + cycle_length]
                if abs(left - right) > tolerance:
                    repeated = False
                    break
            if repeated:
                return start_index, cycle_length
    return None


def fixed_points(func: Callable[[Number], Number], candidates: Iterable[Number]) -> List[Number]:
    """Return candidate points x such that f(x) == x."""

    return [x for x in candidates if func(x) == x]


def cycle_points(
    func: Callable[[Number], Number],
    candidates: Iterable[Number],
    period: int,
) -> List[Number]:
    """Return candidate points whose forward orbit closes after `period` steps."""

    results: List[Number] = []
    for x in candidates:
        value = x
        for _ in range(period):
            value = func(value)
        if value == x:
            results.append(x)
    return results


def sample_integer_orbits(
    start_values: Iterable[int],
    steps: int,
) -> dict[int, List[Number]]:
    """Generate integer orbits for quick experiments."""

    orbits: dict[int, List[Number]] = {}
    for start in start_values:
        orbits[start] = iterate_map(one_dimensional_map, start, steps)
    return orbits


@dataclass(frozen=True)
class OrbitSummary:
    start: Number
    orbit: List[Number]
    cycle: Tuple[int, int] | None


def summarize_orbit(start: Number, steps: int) -> OrbitSummary:
    """Convenience wrapper for quick CLI output."""

    orbit = iterate_map(one_dimensional_map, start, steps)
    cycle = detect_cycle(orbit)
    return OrbitSummary(start=start, orbit=orbit, cycle=cycle)
