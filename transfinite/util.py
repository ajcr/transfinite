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
    if ordinal.coefficient != 1:
        term += rf"\cdot{as_latex(ordinal.coefficient)}"
    if ordinal.addend != 0:
        term += f"+{as_latex(ordinal.addend)}"
    return term


class LatexRepr:
    """
    Render LaTeX strings returned by methods.

    Jupyter hooks into a object's _repr_latex_ method to
    determine whether to render it as LaTeX.

    """

    def __init__(self, latex_string):
        self.latex = latex_string

    @classmethod
    def from_factors(cls, fs):
        fs_latex = []

        for ordinal, exponent in fs:

            if is_finite_ordinal(ordinal):
                fs_latex.append(str(ordinal))

            # Put parentheses around the factor if the exponent is
            # greater than 1, or if ordinal.addend is greater than 0
            #
            #   (w, 1)        -> w
            #   (w, 2)        -> (w)^2
            #   (w + 1, 1)    -> (w + 1)
            #   (w + 1, 2)    -> (w + 1)^2
            #   (w**2 + 1, 1) -> (w^2 + 1)
            #   (w**2 + 1, 3) -> (w^2 + 1)^3
            #
            # Note that since factors are prime, there are some cases
            # that do not need to be covered here (e.g. w*n).

            else:
                latex_ordinal = as_latex(ordinal)

                if ordinal.addend > 0 or exponent > 1:
                    f = rf"\left({latex_ordinal}\right)"
                else:
                    f = latex_ordinal

                if exponent > 1:
                    f += f"^{{{exponent}}}"

                fs_latex.append(f)

        return cls(r"\cdot".join(fs_latex))

    def __str__(self):
        return f"${self.latex}$"

    def __repr__(self):
        return str(self)

    def _repr_latex_(self):
        return str(self)
