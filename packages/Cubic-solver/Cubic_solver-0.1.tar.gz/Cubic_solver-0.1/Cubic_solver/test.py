import unittest
from Cubic_Function import Cubic_Function

class TestCubicEquation(unittest.TestCase):

    def test_get_p_and_q(self):
        # Test case 1: a=1, b=2, c=3, d=4
        eqn1 = cubic_equation(1, 2, 3, 4)
        p, q = eqn1.get_p_and_q()
        self.assertAlmostEqual(p, -1.0)
        self.assertAlmostEqual(q, -7.0)

        # Test case 2: a=2, b=-1, c=0, d=-3
        eqn2 = cubic_equation(2, -1, 0, -3)
        p, q = eqn2.get_p_and_q()
        self.assertAlmostEqual(p, 0.0)
        self.assertAlmostEqual(q, 1.5)

    def test_find_roots(self):
        # Test case 1: a=1, b=2, c=3, d=4
        eqn1 = cubic_equation(1, 2, 3, 4)
        roots = eqn1.find_roots()
        self.assertAlmostEqual(roots[0], -1.6506291914393887 + 0j)
        self.assertAlmostEqual(roots[1], 0.32531459571969436 - 1.290862968962878j)
        self.assertAlmostEqual(roots[2], 0.32531459571969436 + 1.290862968962878j)

        # Test case 2: a=2, b=-1, c=0, d=-3
        eqn2 = cubic_equation(2, -1, 0, -3)
        roots = eqn2.find_roots()
        self.assertAlmostEqual(roots[0], 1.5 + 0j)
        self.assertAlmostEqual(roots[1], -0.7500000000000001 + 1.299038105676658j)
        self.assertAlmostEqual(roots[2], -0.7500000000000001 - 1.299038105676658j)

    def test_plot_cubic(self):
        # Test case 1: a=1, b=2, c=3, d=4
        eqn1 = cubic_equation(1, 2, 3, 4)
        eqn1.plot_cubic()

        # Test case 2: a=2, b=-1, c=0, d=-3
        eqn2 = cubic_equation(2, -1, 0, -3)
        eqn2.plot_cubic()