"""
Specialized Gauss quadrature for numerical integration.
"""
__all__ = 'fixed_quad_jacobi',

from typing import Callable

import numpy as np
import numpy.typing as npt

from scipy.special import roots_jacobi


def fixed_quad_jacobi(
    f: Callable[[npt.NDArray[np.float_]], npt.NDArray[np.float_]],
    alpha: float,
    beta: float,
    n: int = 5,
) -> float:
    """
    Compute a definite integral using fixed-order Gauss-Jacobi quadrature.
    """
    x, w = roots_jacobi(n + 1, alpha, beta)
    return w @ f(x)
