import copy
import operator

import pytest

from transfinite.ordinal import Ordinal, OrdinalConstructionError
from transfinite.util import as_latex


@pytest.mark.parametrize(
    "kwargs",
    [
        {"exponent": 0},
        {"exponent": -1},
        {"exponent": -3.14},
        {"exponent": "0"},
        {"copies": 0},
        {"copies": -1},
        {"copies": -3.14},
        {"copies": "0"},
        {"copies": Ordinal()},
        {"addend": -1},
        {"addend": -3.14},
        {"addend": "0"},
        {"exponent": 1, "addend": Ordinal(exponent=1)},
        {"exponent": Ordinal(), "addend": Ordinal(exponent=Ordinal())},
    ],
)
def test_invalid_args_to_class(kwargs):
    with pytest.raises(OrdinalConstructionError):
        Ordinal(**kwargs)


@pytest.mark.parametrize(
    "a",
    [
        # w
        Ordinal(),
        # w**2
        Ordinal(exponent=2),
        # w**w
        Ordinal(exponent=Ordinal()),
        # w**2 * 5
        Ordinal(exponent=2, copies=5),
        # w**2 + w
        Ordinal(exponent=2, addend=Ordinal()),
    ],
)
def test_equals(a):
    assert a == copy.deepcopy(a)


@pytest.mark.parametrize(
    "a,b",
    [
        # w != w**2
        (Ordinal(), Ordinal(exponent=2)),
        # w != w*2
        (Ordinal(), Ordinal(copies=2)),
        # w == w + 2
        (Ordinal(), Ordinal(addend=2)),
    ],
)
def test_not_equals(a, b):
    assert a != b


@pytest.mark.parametrize(
    "a,b",
    [
        # 13 < w
        (13, Ordinal()),
        # w < w**2
        (Ordinal(), Ordinal(exponent=2)),
        # w < w + 2
        (Ordinal(), Ordinal(addend=2)),
        # w < w*9
        (Ordinal(), Ordinal(copies=9)),
        # w < w**w
        (Ordinal(), Ordinal(exponent=Ordinal())),
        # w**3 < w**5
        (Ordinal(exponent=3), Ordinal(exponent=5)),
        # w**3 < w**w
        (Ordinal(exponent=3), Ordinal(exponent=Ordinal())),
        # w**(w+1) < w**w**w
        (
            Ordinal(exponent=Ordinal(addend=1)),
            Ordinal(exponent=Ordinal(exponent=Ordinal())),
        ),
        # w**(w*100) < w**w**w
        (
            Ordinal(exponent=Ordinal(copies=100)),
            Ordinal(exponent=Ordinal(exponent=Ordinal())),
        ),
        # w**w**2 < w**w**w
        (
            Ordinal(exponent=Ordinal(exponent=2)),
            Ordinal(exponent=Ordinal(exponent=Ordinal())),
        ),
        # w**(w+2) + w*3 < w**(w+3)
        (
            Ordinal(exponent=Ordinal(addend=2), addend=Ordinal(copies=3)),
            Ordinal(exponent=Ordinal(exponent=Ordinal(addend=3))),
        ),
    ],
)
def test_less_than(a, b):
    assert a < b


@pytest.mark.parametrize(
    "a,b",
    [
        # w**5 > w**2
        (Ordinal(exponent=5), Ordinal(exponent=2)),
        # w**w > w
        (Ordinal(exponent=Ordinal()), Ordinal()),
        # w**2 > w + 99
        (Ordinal(exponent=2), Ordinal(addend=99)),
        # w**w > w + 99
        (Ordinal(exponent=Ordinal()), Ordinal(addend=99)),
        # w**(w**w + 3) > w + 99
        (Ordinal(exponent=Ordinal(exponent=Ordinal(), addend=3)), Ordinal(addend=99)),
        # w**(w**w + w) > w**(w**w + 2) + 99
        (
            Ordinal(exponent=Ordinal(exponent=Ordinal(), addend=Ordinal())),
            Ordinal(exponent=Ordinal(exponent=Ordinal(), addend=2), addend=99),
        ),
        # w**w > 16
        (Ordinal(exponent=Ordinal()), 16),
    ],
)
def test_greater_than(a, b):
    assert a > b


@pytest.mark.parametrize(
    "a,expected_str,expected_latex",
    [
        # w
        (Ordinal(), "w", r"\omega"),
        # w**5
        (Ordinal(exponent=5), "w**5", r"\omega^{5}"),
        # w**w
        (Ordinal(exponent=Ordinal()), "w**w", r"\omega^{\omega}"),
        # w**(w + 1)
        (Ordinal(exponent=Ordinal(addend=1)), "w**(w + 1)", r"\omega^{\omega+1}"),
        # w**(w*3)
        (
            Ordinal(exponent=Ordinal(copies=3)),
            "w**(w*3)",
            r"\omega^{\omega\cdot3}",
        ),
        # w + 99
        (Ordinal(addend=99), "w + 99", r"\omega+99"),
        # w**(w**5 + w*3 + 66) * 5
        (
            Ordinal(
                exponent=Ordinal(exponent=5, addend=Ordinal(copies=3, addend=66)),
                copies=5,
            ),
            "w**(w**5 + w*3 + 66)*5",
            r"\omega^{\omega^{5}+\omega\cdot3+66}\cdot5",
        ),
    ],
)
def test_as_string(a, expected_str, expected_latex):
    assert str(a) == expected_str
    assert as_latex(a) == expected_latex


@pytest.mark.parametrize(
    "a,b,expected",
    [
        # (w) + 0 == w
        (Ordinal(), 0, Ordinal()),
        # 0 + (w) == w
        (0, Ordinal(), Ordinal()),
        # (w) + 1 == w + 1
        (Ordinal(), 1, Ordinal(addend=1)),
        # (w**3 + w) + 2 == w**3 + w + 2
        (
            Ordinal(exponent=Ordinal(exponent=3), addend=Ordinal()),
            2,
            Ordinal(exponent=Ordinal(exponent=3), addend=Ordinal(addend=2)),
        ),
        # 1 + w == w
        (1, Ordinal(), Ordinal()),
        # w + w**3 == w**3
        (Ordinal(), Ordinal(exponent=3), Ordinal(exponent=3)),
        # (w) + (w) == w*2
        (Ordinal(), Ordinal(), Ordinal(copies=2)),
        # (w*12 + 2) + (w*7) == w*19
        (
            Ordinal(copies=12, addend=2),
            Ordinal(copies=7),
            Ordinal(copies=19),
        ),
        # (w**2 + w + 2) + 2 == w**2 + w + 4
        (
            Ordinal(exponent=2, addend=Ordinal(addend=2)),
            2,
            Ordinal(exponent=2, addend=Ordinal(addend=4)),
        ),
        # (w**2 + w + 2) + (w*7 + 3) == w**2 + w*8 + 3
        (
            Ordinal(exponent=2, addend=Ordinal(addend=2)),
            Ordinal(copies=7, addend=3),
            Ordinal(exponent=2, addend=Ordinal(copies=8, addend=3)),
        ),
        # (w**2 + w + 2) + (w**9 + w*7 + 3) == w**9 + w*7 + 3
        (
            Ordinal(exponent=2, addend=Ordinal(addend=2)),
            Ordinal(copies=7, addend=3),
            Ordinal(exponent=2, addend=Ordinal(copies=8, addend=3)),
        ),
        # (w**w + w*12 + 2) + (w**w + w*7) == w**w*2 + w*7
        (
            Ordinal(exponent=Ordinal(), addend=Ordinal(copies=12, addend=2)),
            Ordinal(exponent=Ordinal(), addend=Ordinal(copies=7)),
            Ordinal(exponent=Ordinal(), copies=2, addend=Ordinal(copies=7)),
        ),
        # (w**5 + w**3 + 1) + (w**4 + w**2) == w**5 + w**4 + w**2
        (
            Ordinal(exponent=5, addend=Ordinal(exponent=3, addend=1)),
            Ordinal(exponent=4, addend=Ordinal(exponent=2)),
            Ordinal(exponent=5, addend=Ordinal(exponent=4, addend=Ordinal(exponent=2))),
        ),
        # (w**(w*5) + w) + (w**(w*5) + w) == w**(w*5)*2 + w
        (
            Ordinal(exponent=Ordinal(copies=5), addend=Ordinal()),
            Ordinal(exponent=Ordinal(copies=5), addend=Ordinal()),
            Ordinal(exponent=Ordinal(copies=5), copies=2, addend=Ordinal()),
        ),
    ],
)
def test_addition(a, b, expected):
    assert a + b == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        # (w) * 0 == 0
        (Ordinal(), 0, 0),
        # 0 * (w) == 0
        (0, Ordinal(), 0),
        # (w) * 1 == w
        (Ordinal(), 1, Ordinal()),
        # (w) * 2 == w*2
        (Ordinal(), 2, Ordinal(copies=2)),
        # 2 * (w) == w
        (2, Ordinal(), Ordinal()),
        # 2 * (w + 1) == w + 2
        (2, Ordinal(addend=1), Ordinal(addend=2)),
        # (w + 1) * 2 == w*2 + 1
        (Ordinal(addend=1), 2, Ordinal(copies=2, addend=1)),
        # (w + 9) * 2 == w*2 + 9
        (Ordinal(addend=9), 2, Ordinal(copies=2, addend=9)),
        # (w + 9) * 3 == w*3 + 9
        (Ordinal(addend=9), 3, Ordinal(copies=3, addend=9)),
        # (w) * (w) == w**2
        (Ordinal(), Ordinal(), Ordinal(exponent=2)),
        # (w) * (w + 1) == w**2 + w
        (Ordinal(), Ordinal(addend=1), Ordinal(exponent=2, addend=Ordinal())),
        # (w + 1) * (w + 1) == w**2 + w + 1
        (
            Ordinal(addend=1),
            Ordinal(addend=1),
            Ordinal(exponent=2, addend=Ordinal(addend=1)),
        ),
        # (w**2 + w + 1) * (w + 1) == w**3 + w**2 + w + 1
        (
            Ordinal(exponent=2, addend=Ordinal(addend=1)),
            Ordinal(addend=1),
            Ordinal(exponent=3, addend=Ordinal(exponent=2, addend=Ordinal(addend=1))),
        ),
        # (w*3) * (w*3) == w**2*3
        (
            Ordinal(copies=3),
            Ordinal(copies=3),
            Ordinal(exponent=2, copies=3),
        ),
        # (w**5) * (w) == w**6
        (Ordinal(exponent=5), Ordinal(), Ordinal(exponent=6)),
        # (w**2) * (w**7) == w**9
        (Ordinal(exponent=2), Ordinal(exponent=7), Ordinal(exponent=9)),
        # (w + 5) * (w + 2) == w**2 + w*2 + 5
        (
            Ordinal(addend=5),
            Ordinal(addend=2),
            Ordinal(exponent=2, addend=Ordinal(copies=2, addend=5)),
        ),
        # (w**2 + w + 1) * (w*2 + 2) == w**3*2 + w**2*2 + w + 1
        (
            Ordinal(exponent=2, addend=Ordinal(addend=1)),
            Ordinal(copies=2, addend=2),
            Ordinal(
                exponent=3,
                copies=2,
                addend=Ordinal(exponent=2, copies=2, addend=Ordinal(addend=1)),
            ),
        ),
        # (w**w) * (w) == w**(w+1)
        (Ordinal(exponent=Ordinal()), Ordinal(), Ordinal(exponent=Ordinal(addend=1))),
        # (w**w) * (w+2) == w**(w+1) + w**w*2
        (
            Ordinal(exponent=Ordinal()),
            Ordinal(addend=2),
            Ordinal(
                exponent=Ordinal(addend=1),
                addend=Ordinal(exponent=Ordinal(), copies=2),
            ),
        ),
        # 3 * (w*2 + 4) == w*2 + 12
        (3, Ordinal(copies=2, addend=4), Ordinal(copies=2, addend=12)),
        # (w*3 + 4) * (w*3) == w**2*3
        (
            Ordinal(copies=3, addend=4),
            Ordinal(copies=3),
            Ordinal(exponent=2, copies=3),
        ),
        # (w + 1) * (w**2) == w**3
        (Ordinal(addend=1), Ordinal(exponent=2), Ordinal(exponent=3)),
        # w**(w**(w*5) + w) * w**(w**(w*5) + w) == w**(w**(w*5)*2+w)
        (
            Ordinal(
                exponent=Ordinal(exponent=Ordinal(copies=5), addend=Ordinal())
            ),
            Ordinal(
                exponent=Ordinal(exponent=Ordinal(copies=5), addend=Ordinal())
            ),
            Ordinal(
                exponent=Ordinal(
                    exponent=Ordinal(copies=5), copies=2, addend=Ordinal()
                )
            ),
        ),
    ],
)
def test_multiplication(a, b, expected):
    assert a * b == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        # (w) ** 0 == 0
        (Ordinal(), 0, 1),
        # (w) ** 1 == w
        (Ordinal(), 1, Ordinal()),
        # (w) ** 2 == w**2
        (Ordinal(), Ordinal(), Ordinal(exponent=Ordinal())),
        # (w) ** (w) == w**w
        (Ordinal(exponent=2), 2, Ordinal(exponent=4)),
        # (w + 1) ** 2 == w**2 + w + 1
        (Ordinal(addend=1), 2, Ordinal(exponent=2, addend=Ordinal(addend=1))),
        # (w + 1) ** 3 == w**3 + w**2 + w + 1
        (
            Ordinal(addend=1),
            3,
            Ordinal(exponent=3, addend=Ordinal(exponent=2, addend=Ordinal(addend=1))),
        ),
        # (w + 1) ** w == w**w
        (Ordinal(addend=1), Ordinal(), Ordinal(exponent=Ordinal())),
        # 0 ** (w) == 0
        (0, Ordinal(), 0),
        # 1 ** (w) == 1
        (1, Ordinal(), 1),
        # 2 ** (w) == w
        (2, Ordinal(), Ordinal()),
        # 7 ** (w) == w
        (7, Ordinal(), Ordinal()),
        # 2 ** (w*6) == w**6
        (2, Ordinal(copies=6), Ordinal(exponent=6)),
        # 2 ** (w + 1) == w*2
        (2, Ordinal(addend=1), Ordinal(copies=2)),
        # 5 ** (w + 2) == w*25
        (5, Ordinal(addend=2), Ordinal(copies=25)),
        # 2 ** (w**w) == w**w**w
        (2, Ordinal(exponent=Ordinal()), Ordinal(Ordinal(exponent=Ordinal()))),
        # 2 ** (w**9) == w**w**8
        (2, Ordinal(exponent=9), Ordinal(Ordinal(exponent=8))),
        # 2 ** (w**w + w*3 + 9) == w**(w**w + 3)*512
        (
            2,
            Ordinal(exponent=Ordinal(), addend=Ordinal(copies=3, addend=9)),
            Ordinal(exponent=Ordinal(exponent=Ordinal(), addend=3), copies=512),
        ),
        # 2 ** (w**w**w) == w**w**w**w
        (
            2,
            Ordinal(exponent=Ordinal(exponent=Ordinal())),
            Ordinal(exponent=Ordinal(exponent=Ordinal(exponent=Ordinal()))),
        ),
        # 3 ** (w**w + 1) == (w**w**w)*3
        (
            3,
            Ordinal(exponent=Ordinal(), addend=1),
            Ordinal(exponent=Ordinal(exponent=Ordinal()), copies=3),
        ),
        # 2**(w**2 + w) == w**(w + 1)
        (2, Ordinal(exponent=2, addend=Ordinal()), Ordinal(exponent=Ordinal(addend=1))),
        # 2**(w**2 + 3) == w**w * 8
        (2, Ordinal(exponent=2, addend=3), Ordinal(exponent=Ordinal(), copies=8)),
        # 2**(w**3 * 7) == w**(w**2 * 7)
        (
            2,
            Ordinal(exponent=3, copies=7),
            Ordinal(exponent=Ordinal(exponent=2, copies=7)),
        ),
        # 2**(w**3 * 7 + 5) == w**(w**2 * 7) * 32
        (
            2,
            Ordinal(exponent=3, copies=7, addend=5),
            Ordinal(exponent=Ordinal(exponent=2, copies=7), copies=32),
        ),
        # (w**(w**(w*5) + w**w + 2)) ** 2 == w**(w**(w*5)*2+w**w+2)
        (
            Ordinal(
                exponent=Ordinal(
                    exponent=Ordinal(copies=5),
                    addend=Ordinal(exponent=Ordinal(), addend=2),
                )
            ),
            2,
            Ordinal(
                exponent=Ordinal(
                    exponent=Ordinal(copies=5),
                    copies=2,
                    addend=Ordinal(exponent=Ordinal(), addend=2),
                )
            ),
        ),
        # (w**(w**(w*5) + w**w + 2)) ** (w + 3) == w**(w**(w*5+1)+w**(w*5)*3+w**w+2)
        (
            Ordinal(
                exponent=Ordinal(
                    exponent=Ordinal(copies=5),
                    addend=Ordinal(exponent=Ordinal(), addend=2),
                )
            ),
            Ordinal(addend=3),
            Ordinal(
                exponent=Ordinal(
                    exponent=Ordinal(copies=5, addend=1),
                    addend=Ordinal(
                        exponent=Ordinal(copies=5),
                        copies=3,
                        addend=Ordinal(exponent=Ordinal(), addend=2),
                    ),
                )
            ),
        ),
    ],
)
def test_power(a, b, expected):
    assert a ** b == expected


@pytest.mark.parametrize(
    "a,expected",
    [
        (Ordinal(), True),
        (Ordinal(addend=1), False),
        (Ordinal(exponent=Ordinal(), addend=1), False),
        (Ordinal(exponent=Ordinal()), True),
        (Ordinal(exponent=Ordinal(), addend=Ordinal(addend=3)), False),
        (Ordinal(exponent=Ordinal(), addend=Ordinal(copies=3)), True),
    ],
)
def test_is_limit(a, expected):
    assert a.is_limit() is expected


@pytest.mark.parametrize(
    "op",
    [
        operator.add,
        operator.mul,
        operator.pow,
        operator.lt,
        operator.gt,
        operator.ge,
        operator.le,
    ],
)
@pytest.mark.parametrize(
    "a,expected_error",
    [(-2, TypeError), (2.1, TypeError), ("2", TypeError), (7j, TypeError)],
)
def test_invalid_types_operation(op, a, expected_error):
    with pytest.raises(expected_error):
        op(Ordinal(), a)
        op(a, Ordinal())


@pytest.mark.parametrize(
    "a,expected",
    [
        ## Primes
        # w
        (Ordinal(), True),
        # w + 1
        (Ordinal(addend=1), True),
        # w**2 + 1
        (Ordinal(exponent=2, addend=1), True),
        # w**3 + 1
        (Ordinal(exponent=3, addend=1), True),
        # w**w
        (Ordinal(exponent=Ordinal()), True),
        # w**w + 1
        (Ordinal(exponent=Ordinal(), addend=1), True),
        # w**(w + 1) + 1
        (Ordinal(exponent=Ordinal(addend=1), addend=1), True),
        # w**w**w + 1
        (Ordinal(exponent=Ordinal(exponent=Ordinal())), True),
        # w**w**(w+1)
        (Ordinal(exponent=Ordinal(exponent=Ordinal(addend=1))), True),
        # w**w**(w*2)
        (Ordinal(exponent=Ordinal(exponent=Ordinal(copies=2))), True),
        ## Composites
        # w + 2  [2 * (w+1)]
        (Ordinal(addend=2), False),
        # w*2  [w * 2]
        (Ordinal(copies=2), False),
        # w*2 + 1  [(w+1) * 2]
        (Ordinal(copies=2, addend=1), False),
        # w*2 + 3  [3 * (w+1) * 2]
        (Ordinal(copies=2, addend=3), False),
        # w**2  [w * w]
        (Ordinal(exponent=2), False),
        # w**2 + w   [w * (w**2 + 1)]
        (Ordinal(exponent=2, addend=Ordinal()), False),
        # w**(w*2)  [w**w * w**w]
        (Ordinal(exponent=Ordinal(copies=2)), False),
        # w**(w+1)  [w**w * w]
        (Ordinal(exponent=Ordinal(addend=1)), False),
    ],
)
def test_is_prime(a, expected):
    assert a.is_prime() is expected


@pytest.mark.parametrize(
    "a,expected",
    [
        # w
        (Ordinal(), True),
        # w + 1
        (Ordinal(addend=1), False),
        # w**2 + 1
        (Ordinal(exponent=2, addend=1), False),
        # w**w
        (Ordinal(exponent=Ordinal()), True),
        # w**w + 1
        (Ordinal(exponent=Ordinal(), addend=1), False),
        # w**(w + 1)
        (Ordinal(exponent=Ordinal(addend=1), addend=1), False),
        # w**w**w
        (Ordinal(exponent=Ordinal(exponent=Ordinal())), True),
        # w**w**w + 1
        (Ordinal(exponent=Ordinal(exponent=Ordinal()), addend=1), False),
        # w + 2
        (Ordinal(addend=2), False),
        # w*2
        (Ordinal(copies=2), False),
        # w*2 + 3
        (Ordinal(copies=2, addend=3), False),
    ],
)
def test_is_gamma(a, expected):
    assert a.is_gamma() is expected
