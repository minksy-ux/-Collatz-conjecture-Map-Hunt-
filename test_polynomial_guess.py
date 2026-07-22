import unittest

from polynomial_guess import Quadratic, score_poly, search_best


class PolynomialGuessTest(unittest.TestCase):
    def test_score_poly_detects_fast_failures(self) -> None:
        poly = Quadratic(a=-2, b=3, c=1)
        result = score_poly(poly, steps=12, bound=10**6)
        self.assertIsNotNone(result.nonnegative_break_step)
        self.assertIsNotNone(result.escape_step)
        self.assertGreater(result.score, 0)

    def test_search_with_anchors_returns_candidates(self) -> None:
        top = search_best(
            coeff_min=-3,
            coeff_max=3,
            steps=8,
            bound=1000,
            require_collatz_anchors=True,
            top_k=3,
        )
        self.assertGreaterEqual(len(top), 1)
        for item in top:
            self.assertEqual(item.poly.c, 1)
            self.assertEqual(item.poly.a + item.poly.b + item.poly.c, 2)


if __name__ == "__main__":
    unittest.main()