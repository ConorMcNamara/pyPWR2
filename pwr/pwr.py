from math import sqrt, pow

from scipy.stats import f as f_dist, ncf

from pwr2.utils import _pwr_fb, _pwr_fA, _ss_fa, _ss_fb


def pwr_1way(
        k: int, n: int, alpha: float, f: float, delta: float = None, sigma: float = None, print_pretty: bool = True
) -> float:
    """Calculate power for one-way ANOVA models.

    Parameters
    ----------
    k: int
        Number of groups
    n: int
        Sample size per group
    alpha: float
        Significant level (Type I error probability)
    f: float
        Effect size
    delta: float, default=None
        The smallest difference among k groups
    sigma: float, default=None
        Standard deviation, i.e. square root of variance
    print_pretty: bool, default=True
        Whether we want the results printed or not

    Returns
    -------
    The power of our one-way ANOVA model
    """
    if f is None:
        f = sqrt(((1 / k) * pow(delta / 2, 2) * 2) / pow(sigma, 2))
    lamda = n * k * pow(f, 2)
    q = f_dist.isf(alpha, k - 1, (n - 1) * k)
    pwr = ncf.sf(q, k - 1, (n - 1) * k, lamda)
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
        f: float,
        delta: float = None,
        sigma: float = None,
        B: int = 100,
        print_pretty: bool = True,
) -> int:
    """Calculate sample size for one-way ANOVA models.

    Parameters
    ----------
    k: int
        Number of groups
    alpha: float
        Significant level (Type I error probability)
    power: float
        Type II error probability (Power=1-beta)
    f: float
        Effect size
    delta: float, default=None
        The smallest difference among k groups
    sigma: float, default=None
        Standard deviation, i.e. square root of variance
    B: int, default=100
        Iteration times, default number is 100
    print_pretty: bool, default=True
        Whether we want our results printed or not

    Returns
    -------
    The sample size of our one-way ANOVA model
    """
    if f is None:
        f = sqrt(((1 / k) * pow(delta / 2, 2) * 2) / pow(sigma, 2))
    power_list = []
    beta = 1 - power
    for i in range(1, B + 1):
        n_i = i + 1
        N = n_i * k
        lamda = N * pow(f, 2)
        q = f_dist.isf(alpha, k - 1, (n_i - 1) * k)
        pwr = ncf.sf(q, k - 1, (n_i - 1) * k, lamda)
        power_list.append(pwr)
        if power_list[i - 1] >= (1 - beta):
            break
    ss = len(power_list) + 1
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
        a: float,
        b: float,
        alpha: float,
        size_a: float,
        size_b: float,
        f_a: float,
        f_b: float,
        delta_a: float = None,
        delta_b: float = None,
        sigma_a: float = None,
        sigma_b: float = None,
        print_pretty: bool = True
) -> float:
    """Calculate power for two-way ANOVA models.

    Parameters
    ----------
    a: int
        Number of groups in Factor A
    b: int
        Number of groups in Factor B
    alpha: float
        Significant level (Type I error probability)
    size_a: int
        Sample size per group in Factor A
    size_b: int
        Sample size per group in Factor B
    f_a: float
        Effect size of Factor A
    f_b: float
        Effect size of Factor B
    delta_a: float, default=None
        The smallest difference among a groups in Factor A
    delta_b: float, default=None
        The smallest difference among b groups in Factor B
    sigma_a: float, default=None
        Standard deviation, i.e. square root of variance in Factor A
    sigma_b: float, default=None
        Standard deviation, i.e. square root of variance in Factor B
    print_pretty: bool, default=True
        Whether we want our results printed or not

    Returns
    -------
    The power of our two-way ANOVA model
    """
    pwr_b = _pwr_fb(a, b, alpha, size_b, f_b, delta_b, sigma_b)
    pwr_a = _pwr_fA(a, b, alpha, size_a, f_a, delta_a, sigma_a)
    pwr = min(pwr_a, pwr_b)
    if print_pretty:
        str_print = (
                "\t"
                + "Balanced one-way analysis of variance sample size adjustment "
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
        a: float,
        b: float,
        alpha: float,
        power: float,
        f_a: float,
        f_b: float,
        delta_a: float = None,
        delta_b: float = None,
        sigma_a: float = None,
        sigma_b: float = None,
        B: int = 100,
        print_pretty: bool = True,
) -> int:
    """Calculate sample size for two-way ANOVA models.

    Parameters
    ----------
    a: int
        Number of groups in Factor A
    b: int
        Number of groups in Factor B
    alpha: float
        Significant level (Type I error probability)
    power: float
        Type II error probability (Power=1-beta)
    f_a: float
        Effect size of Factor A
    f_b: float
        Effect size of Factor B
    delta_a: float, default=None
        The smallest difference among a groups in Factor A
    delta_b: float, default=None
        The smallest difference among b groups in Factor B
    sigma_a: float, default=None
        Standard deviation, i.e. square root of variance in Factor A
    sigma_b: float, default=None
        Standard deviation, i.e. square root of variance in Factor B
    B: int, default=100
        Iteration times, default number is 100
    print_pretty: bool, default=True
        Whether we want our results printed or not

    Returns
    -------
    The sample size of our two-way ANOVA model
    """
    beta = 1 - power
    ss_a = _ss_fa(a, b, alpha, beta, f_a, delta_a, sigma_a, B)
    ss_b = _ss_fb(a, b, alpha, beta, f_b, delta_b, sigma_b, B)
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
                + f"NOTE: NOTE: n is number in each group, total sample = {ss * a * b}"
        )
        print(str_print)
    return ss
