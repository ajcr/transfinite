from itertools import groupby

import pytest

from transfinite import w
from transfinite.util import is_finite_ordinal
from transfinite.factorisation import (
    factors,
    subtract,
    factorise_term,
    factorise_term_successor,
)


def multiply_factors(fs):
    """
    Return the product of the factors in the sequence.

    """
    a = 1
    for ordinal, exponent in fs:
        a *= ordinal ** exponent
    return a


@pytest.mark.parametrize(
    "a,b",
    [
        (7, 3),
        (w, 3),
        (w + 1, 3),
        (w ** 2, 1),
        (w ** 2 * 5, 3),
        (w + 1, w),
        (w ** 3, w ** 2),
        (w ** 3, w),
        (w ** 3, w + 1),
        (w ** 3 + w ** 2, w),
        (w ** 3 + w ** 2 + 1, w),
        (w ** 3 + 1, w ** 3),
        (w ** 3 + w, w ** 3 + 5),
        (w ** 3 + w + 1, w ** 3 + 5),
        (w ** 3 * 4, w ** 3 * 2),
        (w ** 3 * 4 + w ** 2, w ** 3 * 2),
        (w ** 3 * 4 + w ** 2, w ** 3 * 2 + w + 1),
    ],
)
def test_subtract(a, b):
    assert b + subtract(a, b) == a


@pytest.mark.parametrize(
    "a",
    [
        w,
        w * 7,
        w ** 2,
        w ** (w + 1),
        w ** (w + 1) * 9,
        w ** w ** 2,
        w ** (w ** 2 + w * 3),
        w ** (w ** w + w * 3 + 6),
        w ** (w ** w + w * 3 + 6) * 19,
        w ** (w ** w ** 2 * 2 + w * 3 + 6) * 19,
        w ** (w ** (w + 1) + w + 6) * 19,
        w ** (w * 2),
        w ** (w * 3 + 1),
        w ** (w ** w * 8 + w * 3 + 1),
    ],
)
def test_factorise_term(a):
    fs = factorise_term(a)
    assert multiply_factors(fs) == a
    assert all(is_finite_ordinal(f) or f.is_prime() for f, _ in fs)


@pytest.mark.parametrize(
    "a", [w, w * 3, w ** 5, w ** 3 * 7, w ** (w * 3), w ** (w * 3) * 2]
)
def test_factorise_term_successor(a):
    fs = factorise_term_successor(a)
    assert multiply_factors(fs) == a + 1
    assert all(is_finite_ordinal(f) or f.is_prime() for f, _ in fs)


@pytest.mark.parametrize(
    "a",
    [
        w,
        w + 1,
        w + 2,
        w * 5 + 16,
        w ** 2,
        w ** 2 * 17 + 3,
        w ** 4 * 8,
        w ** w,
        w ** w + 1,
        w ** w + w,
        w ** (w + 1),
        w ** (w + 1) * 5,
        w ** (w + 1) + 1,
        w ** (w + 1) * 8 + 1,
        w ** w ** 2 + w ** w,
        w ** w ** 2 + w ** w + w ** 3,
        w ** w ** 2 + w ** w + w ** 3 * 7,
        w ** w ** 2 + w ** w + 1,
        w ** w ** 2 + w ** w + 21,
        w ** w ** 2 + w ** w * 7 + 21,
        w ** w ** 2 * 13 + w ** w * 7 + 21,
        w ** w ** w + w ** w ** 2 + w ** (w * 7) + 21,
        w ** w ** w * 4 + w ** w ** 2 + w ** (w * 7) + 21,
        w ** w ** (w * 4) + w ** (w + 1) + w ** w + 13,
        w ** w ** (w * 4) + w ** (w ** 2 + 1) * 7 + w ** w + 13,
        w ** w ** (w * 4 + 2) * 11 + w ** (w ** 2 + w + 1) * 7 + w ** w + 13,
        (w + 1) ** 3,
        (w ** 2 + 1) ** 5,
    ],
)
def test_factors(a):
    fs = factors(a)
    ordinals = [f for f, _ in fs]

    # Check the factorisation is correct
    assert all(
        is_finite_ordinal(f) or f.is_prime() for f in ordinals
    ), "Not all factors are prime"
    assert multiply_factors(fs) == a, "Incorrect factorisation"

    # Check the grouping and order of factors is correct
    grouper = groupby(ordinals, key=lambda x: is_finite_ordinal(x) or x.is_successor())
    groups = [(is_successor, list(ords)) for is_successor, ords in grouper]

    assert len(groups) <= 2, "Factors not ordered by limit/successor"

    # If there are only successor ordinals as factors there is no need to check further
    if len(groups) == 1 and groups[0][0]:
        assert all(
            first != second for first, second in zip(groups[0][1], groups[0][1][1:])
        ), "List of successor factors contains consecutive ordinals that are equal"
        return

    # Otherwise, there are both limit/successor factors: limit must come first and be sorted
    assert (
        groups[0][0] is False
    ), "Limit ordinals do not occur before successor ordinals"
    assert groups[0][1] == sorted(
        groups[0][1], reverse=True
    ), "Successor ordinals not sorted in descending order"
    assert all(
        first != second for first, second in zip(groups[0][1], groups[0][1][1:])
    ), "List of limit factors contains consecutive ordinals that are equal"
