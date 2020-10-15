import pytest

from .omega import Ordinal, w



#def test_as_exponent_terms(ordinal):
#    assert as_exponent_terms(ordinal) == expected


@pytest.mark.parametrize(
    "a",
    [
        Ordinal(),
        Ordinal(exponent=2),
        Ordinal(exponent=Ordinal()),
        Ordinal(exponent=2, coefficient=5),
        Ordinal(exponent=2, addend=Ordinal()),
    ],
)
def test_equals(a):
    assert a == a


@pytest.mark.parametrize(
    "a,b",
    [
        (Ordinal(), Ordinal(2)),
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
        # w^w > 16
        (Ordinal(exponent=Ordinal()), 16),
    ],
)
def test_greater_than(a, b):
    assert a > b
