"""A small collection of falsifiable Collatz-inspired polynomial conjectures."""

from __future__ import annotations

from dataclasses import dataclass

from collatz_maps import Number, detect_cycle, one_dimensional_map


@dataclass(frozen=True)
class Counterexample:
    conjecture: str
    start: int
    escaped_at_step: int
    value: Number
    orbit: list[Number]
    reason: str


def find_short_cycle_counterexample(
    low: int,
    high: int,
    steps: int = 25,
    bound: float = 1e6,
    max_cycle_length: int = 4,
) -> Counterexample | None:
    """Counterexample search for the short-cycle conjecture."""

    conjecture = "every_integer_orbit_enters_a_short_cycle"
    for start in range(low, high + 1):
        orbit: list[Number] = [start]
        value: Number = start
        for step in range(1, steps + 1):
            value = one_dimensional_map(value)
            orbit.append(value)
            cycle = detect_cycle(orbit)
            if cycle is not None and cycle[1] <= max_cycle_length:
                break
            if abs(value) > bound:
                return Counterexample(
                    conjecture=conjecture,
                    start=start,
                    escaped_at_step=step,
                    value=value,
                    orbit=orbit,
                    reason="escaped_bound_before_short_cycle",
                )
    return None


def find_nonnegative_counterexample(
    low: int,
    high: int,
    steps: int = 25,
) -> Counterexample | None:
    """Counterexample search for the nonnegative-invariance conjecture."""

    conjecture = "nonnegative_integer_orbits_stay_nonnegative"
    for start in range(low, high + 1):
        if start < 0:
            continue
        orbit: list[Number] = [start]
        value: Number = start
        for step in range(1, steps + 1):
            value = one_dimensional_map(value)
            orbit.append(value)
            if value < 0:
                return Counterexample(
                    conjecture=conjecture,
                    start=start,
                    escaped_at_step=step,
                    value=value,
                    orbit=orbit,
                    reason="negative_value_found",
                )
    return None


def find_bounded_growth_counterexample(
    low: int,
    high: int,
    steps: int = 25,
    bound: float = 100.0,
) -> Counterexample | None:
    """Counterexample search for a bounded-growth conjecture."""

    conjecture = "integer_orbits_remain_within_a_fixed_bound"
    for start in range(low, high + 1):
        orbit: list[Number] = [start]
        value: Number = start
        for step in range(1, steps + 1):
            value = one_dimensional_map(value)
            orbit.append(value)
            if abs(value) > bound:
                return Counterexample(
                    conjecture=conjecture,
                    start=start,
                    escaped_at_step=step,
                    value=value,
                    orbit=orbit,
                    reason="bound_exceeded",
                )
    return None


def find_fast_cycle_counterexample(
    low: int,
    high: int,
    steps: int = 12,
) -> Counterexample | None:
    """Counterexample search for the claim that every orbit cycles quickly."""

    conjecture = "integer_orbits_enter_a_cycle_within_a_small_number_of_steps"
    for start in range(low, high + 1):
        orbit: list[Number] = [start]
        value: Number = start
        for step in range(1, steps + 1):
            value = one_dimensional_map(value)
            orbit.append(value)
            if detect_cycle(orbit) is not None:
                break
        else:
            return Counterexample(
                conjecture=conjecture,
                start=start,
                escaped_at_step=steps,
                value=value,
                orbit=orbit,
                reason="no_cycle_within_step_limit",
            )
    return None


CONJECTURES = {
    "short_cycle": (
        "Every integer orbit eventually enters a short cycle.",
        find_short_cycle_counterexample,
    ),
    "nonnegative": (
        "Every orbit starting from a nonnegative integer stays nonnegative.",
        find_nonnegative_counterexample,
    ),
    "bounded_growth": (
        "Every integer orbit stays within a fixed absolute bound.",
        find_bounded_growth_counterexample,
    ),
    "fast_cycle": (
        "Every integer orbit enters a cycle within a small number of steps.",
        find_fast_cycle_counterexample,
    ),
}