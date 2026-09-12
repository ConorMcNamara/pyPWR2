import pytest

from pwr2.pwr import pwr_1way, pwr_2way, ss_1way, ss_2way


class TestPwr2:
    @pytest.mark.parametrize(
        "k, n, alpha, f, delta, sigma, expected",
        [
            (5, 15, 0.05, None, 1.5, 1, 0.90740261750501),
            (5, 15, 0.05, 0.4, None, None, 0.771435950291555),
        ],
    )
    def test_pwr2_pwr1way(self, k, n, alpha, f, delta, sigma, expected) -> None:
        assert pwr_1way(k, n, alpha, f, delta, sigma, print_pretty=False) == pytest.approx(expected)

    @pytest.mark.parametrize(
        "a, b, alpha, size_a, size_b, f_a, f_b, delta_a, delta_b, sigma_a, sigma_b, expected",
        [
            (2, 4, 0.05, 10, 10, 0.5, 0.3, None, None, None, None, 0.5782724182),
            (2, 4, 0.05, 8, 8, None, None, 3, 2, 2, 2, 0.6219963876),
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
            a, b, alpha, size_a, size_b, f_a, f_b, delta_a, delta_b, sigma_a, sigma_b, print_pretty=False
        ) == pytest.approx(expected)

    @pytest.mark.parametrize(
        "a, b, alpha, size_a, size_b, f_a, f_b, delta_a, delta_b, sigma_a, sigma_b, expected",
        [
            (3, 3, 0.05, 4, 5, 0.8, 0.4, None, None, None, None, 0.6333554),
            (3, 3, 0.05, 4, 5, None, None, 4, 2, 2, 2, 0.6523857),
            (3, 3, 0.05, 4, 5, 0.8, None, None, 2, None, 2, 0.6523857),
            (3, 3, 0.05, 4, 5, None, 0.4, 4, None, 2, None, 0.6333554),
        ],
    )
    def test_pwr2_pwr2way_unequal_sizes_warns(
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
        with pytest.warns(UserWarning, match="size_a != size_b"):
            result = pwr_2way(
                a, b, alpha, size_a, size_b, f_a, f_b, delta_a, delta_b, sigma_a, sigma_b, print_pretty=False
            )
        assert result == pytest.approx(expected)

    @pytest.mark.parametrize(
        "k, alpha, power, f, delta, sigma, B, expected",
        [(5, 0.05, 0.9, 1.5, None, None, 100, 3), (5, 0.05, 0.9, None, 1.5, 1, 100, 15)],
    )
    def test_pwr2_ss1way(self, k, alpha, power, f, delta, sigma, B, expected) -> None:
        assert ss_1way(k, alpha, power, f, delta, sigma, B, print_pretty=False) == expected

    @pytest.mark.parametrize(
        "a, b, alpha, power, f_a, f_b, delta_a, delta_b, sigma_a, sigma_b, B, expected",
        [
            (3, 3, 0.05, 0.9, 0.4, 0.2, None, None, None, None, 100, 36),
            (3, 3, 0.05, 0.9, None, None, 1, 2, 2, 2, 100, 35),
            (2, 4, 0.05, 0.8, 0.4, 0.3, None, None, None, None, 200, 16),
        ],
    )
    def test_pwr2_ss2way(self, a, b, alpha, power, f_a, f_b, delta_a, delta_b, sigma_a, sigma_b, B, expected) -> None:
        assert (
            ss_2way(a, b, alpha, power, f_a, f_b, delta_a, delta_b, sigma_a, sigma_b, B, print_pretty=False) == expected
        )

    def test_ss1way_raises_on_exhausted_iterations(self) -> None:
        with pytest.raises(ValueError, match=r"Target power .* not achieved"):
            ss_1way(k=5, alpha=0.05, power=0.99, f=0.05, B=5, print_pretty=False)

    def test_ss2way_raises_on_exhausted_iterations(self) -> None:
        with pytest.raises(ValueError, match="not achieved"):
            ss_2way(a=3, b=3, alpha=0.05, power=0.99, f_a=0.05, f_b=0.05, B=5, print_pretty=False)


class TestInputValidation:
    @pytest.mark.parametrize(
        "kwargs, match",
        [
            ({"k": 1, "n": 10, "alpha": 0.05, "f": 0.4}, "k must be at least 2"),
            ({"k": 5, "n": 1, "alpha": 0.05, "f": 0.4}, "n must be at least 2"),
            ({"k": 5, "n": 10, "alpha": 0, "f": 0.4}, "alpha must be between"),
            ({"k": 5, "n": 10, "alpha": 1, "f": 0.4}, "alpha must be between"),
            ({"k": 5, "n": 10, "alpha": 0.05, "f": -0.1}, "f must be positive"),
            ({"k": 5, "n": 10, "alpha": 0.05, "f": None, "sigma": -1}, "sigma must be positive"),
        ],
    )
    def test_pwr1way_validation(self, kwargs, match) -> None:
        with pytest.raises(ValueError, match=match):
            pwr_1way(**kwargs, print_pretty=False)

    @pytest.mark.parametrize(
        "kwargs, match",
        [
            ({"k": 1, "alpha": 0.05, "power": 0.8, "f": 0.4}, "k must be at least 2"),
            ({"k": 5, "alpha": 0.05, "power": 0, "f": 0.4}, "power must be between"),
            ({"k": 5, "alpha": 0.05, "power": 1, "f": 0.4}, "power must be between"),
            ({"k": 5, "alpha": 0.05, "power": 0.8, "f": -0.1}, "f must be positive"),
            ({"k": 5, "alpha": 0.05, "power": 0.8, "f": 0.4, "B": 0}, "B must be at least 1"),
        ],
    )
    def test_ss1way_validation(self, kwargs, match) -> None:
        with pytest.raises(ValueError, match=match):
            ss_1way(**kwargs, print_pretty=False)

    @pytest.mark.parametrize(
        "kwargs, match",
        [
            ({"a": 1, "b": 3, "alpha": 0.05, "size_a": 5, "size_b": 5, "f_a": 0.4, "f_b": 0.3}, "a must be at least 2"),
            ({"a": 3, "b": 1, "alpha": 0.05, "size_a": 5, "size_b": 5, "f_a": 0.4, "f_b": 0.3}, "b must be at least 2"),
            (
                {"a": 3, "b": 3, "alpha": 0.05, "size_a": 1, "size_b": 5, "f_a": 0.4, "f_b": 0.3},
                "size_a must be at least 2",
            ),
            (
                {"a": 3, "b": 3, "alpha": 0.05, "size_a": 5, "size_b": 1, "f_a": 0.4, "f_b": 0.3},
                "size_b must be at least 2",
            ),
            (
                {"a": 3, "b": 3, "alpha": 0.05, "size_a": 5, "size_b": 5, "f_a": -0.1, "f_b": 0.3},
                "f_a must be positive",
            ),
            (
                {"a": 3, "b": 3, "alpha": 0.05, "size_a": 5, "size_b": 5, "f_a": 0.4, "f_b": -0.1},
                "f_b must be positive",
            ),
            (
                {"a": 3, "b": 3, "alpha": 0.05, "size_a": 5, "size_b": 5, "f_a": None, "f_b": 0.3, "delta_a": None},
                "delta_a is required",
            ),
            (
                {
                    "a": 3,
                    "b": 3,
                    "alpha": 0.05,
                    "size_a": 5,
                    "size_b": 5,
                    "f_a": None,
                    "f_b": 0.3,
                    "delta_a": 1,
                    "sigma_a": -1,
                },
                "sigma_a must be positive",
            ),
            (
                {"a": 3, "b": 3, "alpha": 0.05, "size_a": 5, "size_b": 5, "f_a": 0.4, "f_b": None, "delta_b": None},
                "delta_b is required",
            ),
            (
                {
                    "a": 3,
                    "b": 3,
                    "alpha": 0.05,
                    "size_a": 5,
                    "size_b": 5,
                    "f_a": 0.4,
                    "f_b": None,
                    "delta_b": 1,
                    "sigma_b": -1,
                },
                "sigma_b must be positive",
            ),
        ],
    )
    def test_pwr2way_validation(self, kwargs, match) -> None:
        with pytest.raises(ValueError, match=match):
            pwr_2way(**kwargs, print_pretty=False)

    @pytest.mark.parametrize(
        "kwargs, match",
        [
            ({"a": 1, "b": 3, "alpha": 0.05, "power": 0.8, "f_a": 0.4, "f_b": 0.3}, "a must be at least 2"),
            ({"a": 3, "b": 3, "alpha": 0.05, "power": 0, "f_a": 0.4, "f_b": 0.3}, "power must be between"),
            ({"a": 3, "b": 3, "alpha": 0.05, "power": 0.8, "f_a": 0.4, "f_b": 0.3, "B": 0}, "B must be at least 1"),
        ],
    )
    def test_ss2way_validation(self, kwargs, match) -> None:
        with pytest.raises(ValueError, match=match):
            ss_2way(**kwargs, print_pretty=False)


if __name__ == "__main__":
    pytest.main()
