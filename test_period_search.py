import unittest

from period_search import exact_period_points, minimal_period, orbit_values


def negation_map(x):
    return -x


def identity_map(x):
    return x


class PeriodSearchTest(unittest.TestCase):
    def test_orbit_values(self) -> None:
        self.assertEqual(orbit_values(identity_map, 3, 2), [3, 3, 3])

    def test_minimal_period(self) -> None:
        self.assertEqual(minimal_period(identity_map, 2, 5), 1)
        self.assertEqual(minimal_period(negation_map, 1, 5), 2)
        self.assertEqual(minimal_period(negation_map, 0, 5), 1)

    def test_exact_period_points(self) -> None:
        candidates = [-1, 0, 1]
        self.assertEqual(exact_period_points(negation_map, candidates, 2), [-1, 1])
        self.assertEqual(exact_period_points(identity_map, candidates, 1), candidates)


if __name__ == "__main__":
    unittest.main()