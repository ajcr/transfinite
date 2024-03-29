from itertools import groupby
from operator import itemgetter

def is_finite_ordinal(n):
    """
    Return True if n is a finite ordinal (non-negative int).

    """
    return isinstance(n, int) and n >= 0


def exp_by_squaring(x, n):
    """
    Compute x**n using exponentiation by squaring.

    """
    if n == 0:
        return 1
    if n == 1:
        return x
    if n % 2 == 0:
        return exp_by_squaring(x * x, n // 2)
    return exp_by_squaring(x * x, (n - 1) // 2) * x


def as_latex(ordinal):
    """
    Convert the Ordinal object to a LaTeX string.

    """
    if isinstance(ordinal, int):
        return str(ordinal)
    term = r"\omega"
    if ordinal.exponent != 1:
        term += f"^{{{as_latex(ordinal.exponent)}}}"
    if ordinal.copies != 1:
        term += rf"\cdot{as_latex(ordinal.copies)}"
    if ordinal.addend != 0:
        term += f"+{as_latex(ordinal.addend)}"
    return term


def multiply_factors(factors):
    """
    Return the product of the factors.

    """
    prod = 1
    for ordinal, exponent in factors:
        prod *= ordinal ** exponent
    return prod


def group_factors(factors):
    """
    Return the factors with the exponents of consecutive equal
    ordinals added together.

    """
    grouped_factors = groupby(factors, key=itemgetter(0))
    return [(ordinal, sum(exp for _, exp in fs)) for ordinal, fs in grouped_factors]
