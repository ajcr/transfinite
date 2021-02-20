def is_non_negative_int(n):
    """
    Return True if n is a non-negative integer.

    If n is a negative integer raise a ValueError, else return False.
    """
    return isinstance(n, int) and n >= 0


def as_latex(ordinal):
    """
    Convert the Ordinal object to a LaTeX string.

    """
    if isinstance(ordinal, int):
        return str(ordinal)
    term = r"\omega"
    if ordinal.exponent != 1:
        term += f"^{{{as_latex(ordinal.exponent)}}}"
    if ordinal.coefficient != 1:
        term += rf"\cdot{as_latex(ordinal.coefficient)}"
    if ordinal.addend != 0:
        term += f"+{as_latex(ordinal.addend)}"
    return term


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
