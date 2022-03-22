from collections.abc import Sequence

from transfinite.util import (
    as_latex,
    group_factors,
    is_finite_ordinal,
    multiply_factors,
)


class OrdinalFactors(Sequence):
    """
    Factors of an ordinal.

    Since ordinal multiplication is non-commutative, the order
    that the factors are multiplied in matters, hence this is
    a Sequence object.

    The object must be initialised from a initial sequence of
    (ordinal, exponent) pairs.

    The object has a _repr_latex_ method so that the sequence
    of ordinals and exponents can be rendered in an easy to
    read way in Jupyter.

    """
    def __init__(self, factors):
        self.factors = group_factors(factors)

    def __iter__(self):
        return iter(self.factors)

    def __contains__(self, other):
        return other in (ordinal for ordinal, _ in self.factors)

    def __len__(self):
        return len(self.factors)

    def __getitem__(self, item):
        return self.factors[item]

    def product(self):
        return multiply_factors(self.factors)

    def __str__(self):
        return str(self.factors)

    def __repr__(self):
        return f"OrdinalFactors({str(self)})"

    def _repr_latex_(self):
        latex = self.as_latex()
        return f"${latex}$"

    def as_latex(self):
        """
        Returns a LaTeX string of the factors.

        Put parentheses around a factor if its exponent is
        greater than 1, or if its addend is greater than 0:

          (w, 1)        -> w
          (w, 2)        -> (w)^2
          (w + 1, 1)    -> (w + 1)
          (w + 1, 2)    -> (w + 1)^2
          (w**2 + 1, 1) -> (w^2 + 1)
          (w**2 + 1, 3) -> (w^2 + 1)^3

        Note that since factors are prime, there are some cases
        that do not need to be covered here (e.g. w*n).
        """
        fs_latex = []

        for ordinal, exponent in self.factors:

            if is_finite_ordinal(ordinal):
                fs_latex.append(str(ordinal))
                continue

            latex_ordinal = as_latex(ordinal)

            if ordinal.addend > 0 or exponent > 1:
                f = rf"\left({latex_ordinal}\right)"
            else:
                f = latex_ordinal

            if exponent > 1:
                f += f"^{{{exponent}}}"

            fs_latex.append(f)

        return r"\cdot".join(fs_latex)
