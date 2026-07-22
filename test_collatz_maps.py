import unittest

from collatz_maps import (
    OrbitSummary,
    cycle_points,
    detect_cycle,
    fixed_points,
    iterate_map,
    iterate_vector_map,
    one_dimensional_map,
    parity_tracking_map,
    sample_integer_orbits,
    summarize_orbit,
)


class CollatzMapsTest(unittest.TestCase):
    def test_one_dimensional_map(self) -> None:
        self.assertEqual(one_dimensional_map(0), 1)
        self.assertEqual(one_dimensional_map(1), 2)
        self.assertEqual(one_dimensional_map(2), -1)

    def test_parity_tracking_map(self) -> None:
        self.assertEqual(parity_tracking_map(2, 1), (1, 3))

    def test_iterate_map(self) -> None:
        self.assertEqual(iterate_map(one_dimensional_map, 0, 3), [0, 1, 2, -1])

    def test_iterate_vector_map(self) -> None:
        self.assertEqual(iterate_vector_map(parity_tracking_map, (0, 1), 2), [(0, 1), (1, 1), (1, 2)])

    def test_detect_cycle(self) -> None:
        self.assertEqual(detect_cycle([1, 2, 3, 2, 3]), (1, 2))
        self.assertIsNone(detect_cycle([1, 2, 3, 4]))

    def test_fixed_points_and_cycles(self) -> None:
        candidates = [-2, -1, 0, 1, 2]
        identity_map = lambda x: x
        self.assertEqual(fixed_points(identity_map, candidates), candidates)
        self.assertEqual(cycle_points(identity_map, candidates, 1), candidates)

    def test_sample_integer_orbits(self) -> None:
        orbits = sample_integer_orbits([0, 1], 2)
        self.assertEqual(orbits[0], [0, 1, 2])
        self.assertEqual(orbits[1], [1, 2, -1])

    def test_summarize_orbit(self) -> None:
        summary = summarize_orbit(0, 3)
        self.assertIsInstance(summary, OrbitSummary)
        self.assertEqual(summary.start, 0)
        self.assertEqual(summary.orbit, [0, 1, 2, -1])
        self.assertIsNone(summary.cycle)


if __name__ == "__main__":
    unittest.main()
