from transfinite.util import is_finite_ordinal, as_latex, multiply_factors


class OrdinalFactors:
    """
    Sequence object representing the factorisation of an ordinal.

    """

    def __init__(self, factors):
        """
        Initialise the object from a sequence of factors.

        Each element of the sequence must be a (ordinal, exponent) pair.

        """
        self.factors = factors

    @property
    def ordinals(self):
        return [ordinal for ordinal, _ in self.factors]

    def __str__(self):
        return str(self.factors)

    def __repr__(self):
        return f"OrdinalFactors({str(self)})"

    def _repr_latex_(self):
        return f"${self.as_latex()}$"

    def __getitem__(self, item):
        return self.factors[item]

    def __iter__(self):
        return iter(self.factors)

    def __bool__(self):
        return bool(self.factors)

    def __contains__(self, other):
        return other in self.ordinals

    def product(self):
        "Return the product of the factors."
        return multiply_factors(self.factors)

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
