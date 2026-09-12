"""Helper utilities for ANOVA power and sample size calculations."""

from math import pow, sqrt

from scipy.stats import f as f_dist
from scipy.stats import ncf


def _pwr_fA(
    a: int,
    b: int,
    alpha: float,
    size_a: int,
    f_a: float | None,
    delta_a: float,
    sigma_a: float,
) -> float:
    N = size_a * a * b
    if f_a is None:
        f_a = sqrt(((1 / a) * pow(delta_a / 2, 2) * 2) / pow(sigma_a, 2))
    lamda = N * pow(f_a, 2)
    q = f_dist.isf(alpha, a - 1, N - a - b + 1)
    power = ncf.sf(q, a - 1, N - a - b + 1, lamda)
    return float(power)


def _pwr_fB(
    a: int,
    b: int,
    alpha: float,
    size_b: int,
    f_b: float | None,
    delta_b: float,
    sigma_b: float,
) -> float:
    N = size_b * a * b
    if f_b is None:
        f_b = sqrt(((1 / b) * pow(delta_b / 2, 2) * 2) / pow(sigma_b, 2))
    lamda = N * pow(f_b, 2)
    q = f_dist.isf(alpha, b - 1, N - a - b + 1)
    power = ncf.sf(q, b - 1, N - a - b + 1, lamda)
    return float(power)


def _ss_fA(
    a: int,
    b: int,
    alpha: float,
    beta: float,
    f_a: float | None,
    delta_a: float,
    sigma_a: float,
    B: int,
) -> int:
    if f_a is None:
        f_a = sqrt(((1 / a) * pow(delta_a / 2, 2) * 2) / pow(sigma_a, 2))
    lo, hi = 2, B + 1
    N_hi = hi * a * b
    q_hi = f_dist.isf(alpha, a - 1, N_hi - a - b + 1)
    if ncf.sf(q_hi, a - 1, N_hi - a - b + 1, N_hi * pow(f_a, 2)) < 1 - beta:
        raise ValueError(f"Target power not achieved within B={B} iterations (max n={B + 1}). Increase B.")
    while lo < hi:
        mid = (lo + hi) // 2
        N = mid * a * b
        lamda = N * pow(f_a, 2)
        q = f_dist.isf(alpha, a - 1, N - a - b + 1)
        if ncf.sf(q, a - 1, N - a - b + 1, lamda) >= 1 - beta:
            hi = mid
        else:
            lo = mid + 1
    return lo


def _ss_fB(
    a: int,
    b: int,
    alpha: float,
    beta: float,
    f_b: float | None,
    delta_b: float,
    sigma_b: float,
    B: int,
) -> int:
    if f_b is None:
        f_b = sqrt(((1 / b) * pow(delta_b / 2, 2) * 2) / pow(sigma_b, 2))
    lo, hi = 2, B + 1
    N_hi = hi * a * b
    q_hi = f_dist.isf(alpha, b - 1, N_hi - a - b + 1)
    if ncf.sf(q_hi, b - 1, N_hi - a - b + 1, N_hi * pow(f_b, 2)) < 1 - beta:
        raise ValueError(f"Target power not achieved within B={B} iterations (max n={B + 1}). Increase B.")
    while lo < hi:
        mid = (lo + hi) // 2
        N = mid * a * b
        lamda = N * pow(f_b, 2)
        q = f_dist.isf(alpha, b - 1, N - a - b + 1)
        if ncf.sf(q, b - 1, N - a - b + 1, lamda) >= 1 - beta:
            hi = mid
        else:
            lo = mid + 1
    return lo
