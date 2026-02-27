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


def _pwr_fb(
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
        f_b = sqrt(((1 / a) * pow(delta_b / 2, 2) * 2) / pow(sigma_b, 2))
    lamda = N * pow(f_b, 2)
    q = f_dist.isf(alpha, a - 1, N - a - b + 1)
    power = ncf.sf(q, a - 1, N - a - b + 1, lamda)
    return float(power)


def _ss_fa(
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
    power = []
    for i in range(1, B + 1):
        n_i = i + 1
        N = n_i * a * b
        lamda = N * pow(f_a, 2)
        q = f_dist.isf(alpha, a - 1, N - a - b + 1)
        pwr = ncf.sf(q, a - 1, N - a - b + 1, lamda)
        power.append(pwr)
        if power[i - 1] >= 1 - beta:
            break
    ss = len(power) + 1
    return ss


def _ss_fb(
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
        f_b = sqrt(((1 / a) * pow(delta_b / 2, 2) * 2) / pow(sigma_b, 2))
    power = []
    for i in range(1, B + 1):
        n_i = i + 1
        N = n_i * a * b
        lamda = N * pow(f_b, 2)
        q = f_dist.isf(alpha, a - 1, N - a - b + 1)
        pwr = ncf.sf(q, a - 1, N - a - b + 1, lamda)
        power.append(pwr)
        if power[i - 1] >= 1 - beta:
            break
    ss = len(power) + 1
    return ss
