"""
Fitting univariate probablity distributions with the Method of L-moments (L-MM).
"""
from typing import Any, TypeAlias, TypeVar, cast

import numpy as np
import numpy.typing as npt
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from scipy.special import btdtr, loggamma as lgamma

from lmo import l_ratio

T = TypeVar('T')

LStats4: TypeAlias = tuple[T, T, T, T]


def _t4_norm() -> float:
    # approx 0.1226
    return 30 * np.arctan(np.sqrt(2)) / np.pi - 9


def _l2_t(df: float | npt.NDArray[np.float_]) -> float | npt.NDArray[np.float_]:
    # 8.127
    return np.pi * np.exp(
        np.log(2) * (6 - 4 * df)
        + np.log(df) / 2
        + lgamma(2 * df - 2)
        - 4 * lgamma(df / 2)
    )

def _t4_t(df: float) -> float:
    # 8.129
    def _g(x: float) -> float:
        # btdtr is the CDF of the Beta distribution
        return (
            (1 - x) ** (df - 3 / 2)
            * btdtr(1 / 2, df / 2, x) ** 2
            / np.sqrt(x)
        )
    return (
        7.5
        * np.exp(lgamma(df) - lgamma(.5) - lgamma(df - .5))
        * quad(_g, 0, 1)[0]
        - 1.5
    )

def _inv_t4_t(t4: float) -> float:
    t4_min = _t4_norm()
    if t4 > 1 or t4 < 0:
        return np.nan
    if t4 <= t4_min:
        return np.inf

    # found using precise numerical interpolation
    c = 0.32736451422315
    phi = np.exp(t4 - t4_min)
    return (c * phi + 1) / (phi - 1)


def stats_t(
    df: npt.ArrayLike,
    /,
    trim: tuple[int, int] = (0, 0),
) -> LStats4[float] | LStats4[npt.NDArray[np.float_]]:
    if trim != (0, 0):
        raise NotImplementedError

    nu = np.asarray(df)[()]

    l2 = _l2_t(nu)

    if np.isscalar(nu):
        t4 = _t4_t(cast(float, nu))
    else:
        t4 = np.empty_like(nu, dtype=np.float_)
        for i in np.ndindex(nu.shape):
            t4[i] = _t4_t(nu[i])

    return .0 * nu, l2, .0 * nu, t4


def fit_t(
    a: npt.ArrayLike,
    /,
    df: float | None = None,
    df_max: float = 1000,
    trim: tuple[int, int] = (0, 0),
    **kwargs: Any,
) -> tuple[float, float, float]:

    l1, l2, t4 = l_ratio(a, [1, 2, 4], [0, 0, 2], trim, **kwargs)

    if df is None:
        # TODO: pre-compute & interpolate
        res = minimize_scalar(
            lambda _df: (t4 - _t4_t(_df))**2,
            bounds=(1., df_max)
        )
        if not res.success:
            raise RuntimeError(res.message)
        nu = res.x
    else:
        nu = df

    # 8.130
    loc = l1

    # 8.131
    scale = l2 / _l2_t(nu)

    return nu, loc, scale
