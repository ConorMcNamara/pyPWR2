"""Power and sample size calculations for one- and two-way ANOVA models."""

import warnings
from math import pow, sqrt

from scipy.stats import f as f_dist
from scipy.stats import ncf

from pwr2.utils import _pwr_fA, _pwr_fB, _ss_fA, _ss_fB


def pwr_1way(
    k: int,
    n: int,
    alpha: float,
    f: float | None,
    delta: float = 0.1,
    sigma: float = 0.1,
    print_pretty: bool = True,
) -> float:
    """Calculate power for one-way ANOVA models.

    Parameters
    ----------
    k : int
        Number of groups
    n : int
        Sample size per group
    alpha : float
        Significant level (Type I error probability)
    f : float
        Effect size
    delta : float, default=0.1
        The smallest difference among k groups
    sigma : float, default=0.1
        Standard deviation, i.e. square root of variance
    print_pretty : bool, default=True
        Whether we want the results printed or not

    Returns
    -------
    The power of our one-way ANOVA model
    """
    if k < 2:
        raise ValueError("k must be at least 2")
    if n < 2:
        raise ValueError("n must be at least 2")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1 exclusive")
    if f is not None and f <= 0:
        raise ValueError("f must be positive")
    if f is None and sigma <= 0:
        raise ValueError("sigma must be positive when f is not provided")
    if f is None:
        f = sqrt(((1 / k) * pow(delta / 2, 2) * 2) / pow(sigma, 2))
    lamda = n * k * pow(f, 2)
    q = f_dist.isf(alpha, k - 1, (n - 1) * k)
    pwr: float = ncf.sf(q, k - 1, (n - 1) * k, lamda)
    if print_pretty:
        str_print = (
            "\t"
            + "Balanced one-way analysis of variance power calculation"
            + "\n" * 2
            + "\t" * 4
            + f"k = {k}"
            + "\n"
            + "\t" * 4
            + f"n = {n}"
            + "\n"
            + "\t"
            + " " * 2
            + f"effect_size = {round(f, 4)}"
            + "\n"
            + "\t"
            + " " * 4
            + f"sig_level = {alpha}"
            + "\n"
            + "\t"
            + " " * 8
            + f"power = {round(pwr, 4)}"
            + "\n" * 2
            + "NOTE: n is number in each group"
            + "\n"
            + f"Total sample = {n * k}"
        )
        print(str_print)
    return pwr


def ss_1way(
    k: int,
    alpha: float,
    power: float,
    f: float | None,
    delta: float = 0.1,
    sigma: float = 0.1,
    B: int = 1000,
    print_pretty: bool = True,
) -> int:
    """Calculate sample size for one-way ANOVA models.

    Parameters
    ----------
    k : int
        Number of groups
    alpha : float
        Significant level (Type I error probability)
    power : float
        Type II error probability (Power=1-beta)
    f : float
        Effect size
    delta : float, default=0.1
        The smallest difference among k groups
    sigma : float, default=0.1
        Standard deviation, i.e. square root of variance
    B : int, default=1000
        Upper bound on the sample size search (max n = B + 1)
    print_pretty : bool, default=True
        Whether we want our results printed or not

    Returns
    -------
    The sample size of our one-way ANOVA model
    """
    if k < 2:
        raise ValueError("k must be at least 2")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1 exclusive")
    if not 0 < power < 1:
        raise ValueError("power must be between 0 and 1 exclusive")
    if f is not None and f <= 0:
        raise ValueError("f must be positive")
    if f is None and sigma <= 0:
        raise ValueError("sigma must be positive when f is not provided")
    if B < 1:
        raise ValueError("B must be at least 1")
    if f is None:
        f = sqrt(((1 / k) * pow(delta / 2, 2) * 2) / pow(sigma, 2))
    lo, hi = 2, B + 1
    N_hi = hi * k
    q_hi = f_dist.isf(alpha, k - 1, (hi - 1) * k)
    if ncf.sf(q_hi, k - 1, (hi - 1) * k, N_hi * pow(f, 2)) < power:
        raise ValueError(f"Target power {power} not achieved within B={B} iterations (max n={B + 1}). Increase B.")
    while lo < hi:
        mid = (lo + hi) // 2
        N = mid * k
        lamda = N * pow(f, 2)
        q = f_dist.isf(alpha, k - 1, (mid - 1) * k)
        if ncf.sf(q, k - 1, (mid - 1) * k, lamda) >= power:
            hi = mid
        else:
            lo = mid + 1
    ss = lo
    if print_pretty:
        str_print = (
            "\t"
            + "Balanced one-way analysis of variance sample size adjustment"
            + "\n" * 2
            + "\t" * 4
            + f"k = {k}"
            + "\n"
            + "\t"
            + " " * 4
            + f"sig_level = {alpha}"
            + "\n"
            + "\t"
            + " " * 8
            + f"power = {power}"
            + "\n"
            + "\t" * 4
            + f"n = {ss}"
            + "\n" * 2
            + "NOTE: n is number in each group"
            + "\n"
            + f"Total sample = {ss * k}"
        )
        print(str_print)
    return ss


def pwr_2way(
    a: int,
    b: int,
    alpha: float,
    size_a: int,
    size_b: int,
    f_a: float | None,
    f_b: float | None,
    delta_a: float = 0.1,
    delta_b: float = 0.1,
    sigma_a: float = 0.1,
    sigma_b: float = 0.1,
    print_pretty: bool = True,
) -> float:
    """Calculate power for two-way ANOVA models.

    Assumes a main-effects-only model (no interaction term). If the analysis
    will include an A*B interaction, the actual error degrees of freedom will
    be smaller, making these power estimates slightly optimistic.

    Parameters
    ----------
    a : int
        Number of groups in Factor A
    b : int
        Number of groups in Factor B
    alpha : float
        Significant level (Type I error probability)
    size_a : int
        Per-cell sample size used for Factor A power calculation
    size_b : int
        Per-cell sample size used for Factor B power calculation
    f_a : float
        Effect size of Factor A
    f_b : float
        Effect size of Factor B
    delta_a : float, default=0.1
        The smallest difference among a groups in Factor A
    delta_b : float, default=0.1
        The smallest difference among b groups in Factor B
    sigma_a : float, default=0.1
        Standard deviation, i.e. square root of variance in Factor A
    sigma_b : float, default=0.1
        Standard deviation, i.e. square root of variance in Factor B
    print_pretty : bool, default=True
        Whether we want our results printed or not

    Returns
    -------
    The power of our two-way ANOVA model
    """
    if a < 2:
        raise ValueError("a must be at least 2")
    if b < 2:
        raise ValueError("b must be at least 2")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1 exclusive")
    if size_a < 2:
        raise ValueError("size_a must be at least 2")
    if size_b < 2:
        raise ValueError("size_b must be at least 2")
    if f_a is not None and f_a <= 0:
        raise ValueError("f_a must be positive")
    if f_b is not None and f_b <= 0:
        raise ValueError("f_b must be positive")
    if f_a is None:
        if delta_a is None:
            raise ValueError("delta_a is required when f_a is not provided")
        if sigma_a is None or sigma_a <= 0:
            raise ValueError("sigma_a must be positive when f_a is not provided")
    if f_b is None:
        if delta_b is None:
            raise ValueError("delta_b is required when f_b is not provided")
        if sigma_b is None or sigma_b <= 0:
            raise ValueError("sigma_b must be positive when f_b is not provided")
    if size_a != size_b:
        warnings.warn(
            "size_a != size_b: power for each factor is computed with a different "
            "total N, which does not correspond to a single balanced design",
            stacklevel=2,
        )
    pwr_a = _pwr_fA(a, b, alpha, size_a, f_a, delta_a, sigma_a)
    pwr_b = _pwr_fB(a, b, alpha, size_b, f_b, delta_b, sigma_b)
    pwr = min(pwr_a, pwr_b)
    if print_pretty:
        str_print = (
            "\t"
            + "Balanced two-way analysis of variance power calculation"
            + "\n" * 2
            + "\t" * 4
            + f"a = {a}"
            + "\n"
            + "\t" * 4
            + f"b = {b}"
            + "\n"
            + "\t" * 3
            + " " * 2
            + f"n_A = {size_a}"
            + "\n"
            + "\t" * 3
            + " " * 2
            + f"n_B = {size_b}"
            + "\n"
            + "\t"
            + " " * 4
            + f"sig_level = {alpha}"
            + "\n"
            + "\t" * 2
            + " " * 2
            + f"power_a = {round(pwr_a, 4)}"
            + "\n"
            + "\t" * 2
            + " " * 2
            + f"power_b = {round(pwr_b, 4)}"
            + "\n"
            + "\t"
            + " " * 8
            + f"power = {round(pwr, 4)}"
            + "\n" * 2
            + "NOTE: power is the minimum power among two factors"
        )
        print(str_print)
    return pwr


def ss_2way(
    a: int,
    b: int,
    alpha: float,
    power: float,
    f_a: float | None,
    f_b: float | None,
    delta_a: float = 0.1,
    delta_b: float = 0.1,
    sigma_a: float = 0.1,
    sigma_b: float = 0.1,
    B: int = 1000,
    print_pretty: bool = True,
) -> int:
    """Calculate sample size for two-way ANOVA models.

    Assumes a main-effects-only model (no interaction term). If the analysis
    will include an A*B interaction, the actual error degrees of freedom will
    be smaller, making these sample size estimates slightly optimistic.

    Parameters
    ----------
    a : int
        Number of groups in Factor A
    b : int
        Number of groups in Factor B
    alpha : float
        Significant level (Type I error probability)
    power : float
        Type II error probability (Power=1-beta)
    f_a : float
        Effect size of Factor A
    f_b : float
        Effect size of Factor B
    delta_a : float, default=0.1
        The smallest difference among a groups in Factor A
    delta_b : float, default=0.1
        The smallest difference among b groups in Factor B
    sigma_a : float, default=0.1
        Standard deviation, i.e. square root of variance in Factor A
    sigma_b : float, default=0.1
        Standard deviation, i.e. square root of variance in Factor B
    B : int, default=1000
        Upper bound on the sample size search (max n = B + 1)
    print_pretty : bool, default=True
        Whether we want our results printed or not

    Returns
    -------
    The per-cell sample size of our two-way ANOVA model
    """
    if a < 2:
        raise ValueError("a must be at least 2")
    if b < 2:
        raise ValueError("b must be at least 2")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1 exclusive")
    if not 0 < power < 1:
        raise ValueError("power must be between 0 and 1 exclusive")
    if f_a is not None and f_a <= 0:
        raise ValueError("f_a must be positive")
    if f_b is not None and f_b <= 0:
        raise ValueError("f_b must be positive")
    if f_a is None:
        if delta_a is None:
            raise ValueError("delta_a is required when f_a is not provided")
        if sigma_a is None or sigma_a <= 0:
            raise ValueError("sigma_a must be positive when f_a is not provided")
    if f_b is None:
        if delta_b is None:
            raise ValueError("delta_b is required when f_b is not provided")
        if sigma_b is None or sigma_b <= 0:
            raise ValueError("sigma_b must be positive when f_b is not provided")
    if B < 1:
        raise ValueError("B must be at least 1")
    beta = 1 - power
    ss_a = _ss_fA(a, b, alpha, beta, f_a, delta_a, sigma_a, B)
    ss_b = _ss_fB(a, b, alpha, beta, f_b, delta_b, sigma_b, B)
    ss = max(ss_a, ss_b)
    if print_pretty:
        str_print = (
            "\t"
            + "Balanced two-way analysis of variance sample size adjustment "
            + "\n" * 2
            + "\t" * 4
            + f"a = {a}"
            + "\n"
            + "\t" * 4
            + f"b = {b}"
            + "\n"
            + "\t"
            + " " * 4
            + f"sig_level = {alpha}"
            + "\n"
            + "\t" * 3
            + f"power = {round(power, 4)}"
            + "\n"
            + "\t" * 4
            + f"n = {ss}"
            + "\n" * 2
            + f"NOTE: n is number in each group, total sample = {ss * a * b}"
        )
        print(str_print)
    return ss
