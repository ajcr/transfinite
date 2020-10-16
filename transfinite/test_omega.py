import pytest

from .omega import Ordinal


@pytest.mark.parametrize(
    "a",
    [
        # w
        Ordinal(),
        # w^2
        Ordinal(exponent=2),
        # w^w
        Ordinal(exponent=Ordinal()),
        # w^2 . 5
        Ordinal(exponent=2, coefficient=5),
        # w^2 + w
        Ordinal(exponent=2, addend=Ordinal()),
    ],
)
def test_equals(a):
    assert a == a


@pytest.mark.parametrize(
    "a,b",
    [
        # w != w^2
        (Ordinal(), Ordinal(exponent=2)),
        # w != w.2
        (Ordinal(), Ordinal(coefficient=2)),
        # w == w + 2
        (Ordinal(), Ordinal(addend=2)),
    ]
)
def test_not_equals(a, b):
    assert a != b


@pytest.mark.parametrize(
    "a,b",
    [
        # 13 < w
        (13, Ordinal()),
        # w < w^2
        (Ordinal(), Ordinal(exponent=2)),
        # w < w + 2
        (Ordinal(), Ordinal(addend=2)),
        # w < w.9
        (Ordinal(), Ordinal(coefficient=9)),
        # w < w^w
        (Ordinal(), Ordinal(exponent=Ordinal())),
        # w^3 < w^5
        (Ordinal(exponent=3), Ordinal(exponent=5)),
        # w^3 < w^w
        (Ordinal(exponent=3), Ordinal(exponent=Ordinal())),
        # w^(w+1) < w^w^w
        (Ordinal(exponent=Ordinal(addend=1)), Ordinal(exponent=Ordinal(exponent=Ordinal()))),
        # w^(w.100) < w^w^w
        (Ordinal(exponent=Ordinal(coefficient=100)), Ordinal(exponent=Ordinal(exponent=Ordinal()))),
        # w^w^2 < w^w^w
        (Ordinal(exponent=Ordinal(exponent=2)), Ordinal(exponent=Ordinal(exponent=Ordinal()))),
        # w^(w+2) + w.3 < w^(w+3)
        (
            Ordinal(exponent=Ordinal(addend=2), addend=Ordinal(coefficient=3)),
            Ordinal(exponent=Ordinal(exponent=Ordinal(addend=3))),
        ),
    ],
)
def test_less_than(a, b):
    assert a < b


@pytest.mark.parametrize(
    "a,b",
    [
        # w^5 > w^2
        (Ordinal(exponent=5), Ordinal(exponent=2)),
        # w^w > w
        (Ordinal(exponent=Ordinal()), Ordinal()),
        # w^2 > w + 99
        (Ordinal(exponent=2), Ordinal(addend=99)),
        # w^w > w + 99
        (Ordinal(exponent=Ordinal()), Ordinal(addend=99)),
        # w^(w^w + 3) > w + 99
        (Ordinal(exponent=Ordinal(exponent=Ordinal(), addend=3)), Ordinal(addend=99)),
        # w^(w^w + w) > w^(w^w + 2) + 99
        (
            Ordinal(exponent=Ordinal(exponent=Ordinal(), addend=Ordinal())),
            Ordinal(exponent=Ordinal(exponent=Ordinal(), addend=2), addend=99),
        ),
        # w^w > 16
        (Ordinal(exponent=Ordinal()), 16),
    ],
)
def test_greater_than(a, b):
    assert a > b


@pytest.mark.parametrize(
    "a,expected",
    [
        # w
        (Ordinal(), r"\omega"),
        # w^5
        (Ordinal(exponent=5), r"\omega^{5}"),
        # w^w > w
        (Ordinal(exponent=Ordinal()), r"\omega^{\omega}"),
        # w + 99
        (Ordinal(addend=99), r"\omega+99"),
        # w^(w^5 + w.3 + 66) . 5
        (
            Ordinal(
                exponent=Ordinal(exponent=5, addend=Ordinal(coefficient=3, addend=66)),
                coefficient=5,
            ),
            r"\omega^{\omega^{5}+\omega\cdot3+66}\cdot5",
        ),
    ],
)
def test_as_latex_string(a, expected):
    assert str(a) == expected
