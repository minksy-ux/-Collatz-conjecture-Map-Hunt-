import unittest

from plot_orbits import ascii_orbit_plot, build_orbit, scale_index


class OrbitPlotTest(unittest.TestCase):
    def test_scale_index(self) -> None:
        self.assertEqual(scale_index(0.0, 0.0, 10.0, 5), 4)
        self.assertEqual(scale_index(10.0, 0.0, 10.0, 5), 0)

    def test_ascii_orbit_plot(self) -> None:
        plot = ascii_orbit_plot([0.0, 1.0, 2.0], height=3)
        self.assertIn("*", plot)
        self.assertIn("range:", plot)
        self.assertIn("|", plot)

    def test_build_orbit(self) -> None:
        self.assertEqual(build_orbit(0.0, 3), [0.0, 1.0, 2.0, -1.0])


if __name__ == "__main__":
    unittest.main()