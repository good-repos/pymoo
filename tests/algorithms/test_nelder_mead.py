import unittest

import numpy as np
from scipy.optimize import minimize as scipy_minimize

from pymoo.algorithms.so_nelder_mead import nelder_mead
from pymoo.factory import get_problem
from pymoo.optimize import minimize


class NelderAndMeadTestTest(unittest.TestCase):

    def test_no_bounds(self):
        problem = get_problem("rastrigin")
        problem.xl = None
        problem.xu = None
        method = nelder_mead(x0=np.array([1, 1]), max_restarts=0)
        minimize(problem, method, verbose=False)

    def test_with_bounds_no_restart(self):
        problem = get_problem("rastrigin")
        method = nelder_mead(x0=np.array([1, 1]), max_restarts=0)
        minimize(problem, method, verbose=False)

    def test_with_bounds_with_restart(self):
        problem = get_problem("rastrigin")
        method = nelder_mead(x0=np.array([1, 1]), max_restarts=2)
        minimize(problem, method, verbose=False)

    def test_against_scipy(self):
        problem = get_problem("rosenbrock")
        problem.xl = None
        problem.xu = None
        x0 = np.array([0.5, 0.5])

        hist_scipy = []

        def fun(x):
            hist_scipy.append(x)
            return problem.evaluate(x)

        scipy_minimize(fun, x0, method='Nelder-Mead')
        hist_scipy = np.array(hist_scipy)

        hist = []

        def callback(x):
            if x.shape == 2:
                hist.extend(x)
            else:
                hist.append(x)

        problem.callback = callback
        minimize(problem, nelder_mead(x0=x0, max_restarts=0))
        hist = np.row_stack(hist)

        n = min(len(hist), len(hist_scipy))
        hist, hist_scipy = hist[:n], hist_scipy[:n]

        self.assertTrue(np.all(hist - hist_scipy < 1e-7))


if __name__ == '__main__':
    unittest.main()