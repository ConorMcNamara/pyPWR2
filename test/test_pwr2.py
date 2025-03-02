import pytest

from pwr.pwr import pwr_1way, pwr_2way, ss_1way, ss_2way


class TestPwr2:
    @pytest.mark.parametrize(
        "k, n, alpha, f, delta, sigma, expected",
        [
            (5, 15, 0.05, None, 1.5, 1, 0.90740261750501),
            (5, 15, 0.05, 0.4, None, None, 0.771435950291555),
        ],
    )
    def test_pwr2_pwr1way(self, k, n, alpha, f, delta, sigma, expected) -> None:
        assert pwr_1way(k, n, alpha, f, delta, sigma) == pytest.approx(expected)

    @pytest.mark.parametrize(
        "a, b, alpha, size_a, size_b, f_a, f_b, delta_a, delta_b, sigma_a, sigma_b, expected",
        [
            (3, 3, 0.05, 4, 5, 0.8, 0.4, None, None, None, None, 0.6333554),
            (3, 3, 0.05, 4, 5, None, None, 4, 2, 2, 2, 0.6523857),
        ],
    )
    def test_pwr2_pwr2way(
            self,
            a,
            b,
            alpha,
            size_a,
            size_b,
            f_a,
            f_b,
            delta_a,
            delta_b,
            sigma_a,
            sigma_b,
            expected,
    ) -> None:
        assert pwr_2way(
            a, b, alpha, size_a, size_b, f_a, f_b, delta_a, delta_b, sigma_a, sigma_b
        ) == pytest.approx(expected)

    @pytest.mark.parametrize(
        "k, alpha, power, f, delta, sigma, B, expected",
        [
            (5, 0.05, 0.9, 1.5, None, None, 100, 3),
            (5, 0.05, 0.9, None, 1.5, 1, 100, 15)
        ]
    )
    def test_pwr2_ss1way(self, k, alpha, power, f, delta, sigma, B, expected) -> None:
        assert ss_1way(k, alpha, power, f, delta, sigma, B) == expected

    @pytest.mark.parametrize(
        "a, b, alpha, power, f_a, f_b, delta_a, delta_b, sigma_a, sigma_b, B, expected",
        [
            (3, 3, 0.05, 0.9, 0.4, 0.2, None, None, None, None, 100, 36),
            (3, 3, 0.05, 0.9, None, None, 1, 2, 2, 2, 100, 35)
        ]
    )
    def test_pwr2_ss2way(self, a, b, alpha, power, f_a, f_b, delta_a, delta_b, sigma_a, sigma_b, B, expected) -> None:
        assert ss_2way(a, b, alpha, power, f_a, f_b, delta_a, delta_b, sigma_a, sigma_b, B) == expected
