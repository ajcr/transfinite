from copy import deepcopy
from functools import total_ordering


@total_ordering
class Ordinal:
    r"""
    An infinite ordinal less than \epsilon_0.

    """
    def __init__(self, exponent=1, coefficient=1, addend=0):
        self.exponent = exponent
        self.coefficient = coefficient
        self.addend = addend
        
    def _repr_latex_(self):
        return rf"${self}$"

    def __repr__(self):
        return str(self).replace(r"\omega", "w").replace(r"\cdot", "*")

    def __str__(self):
        term = r"\omega"

        if self.exponent != 1:
            term += f"^{{{self.exponent}}}"

        if self.coefficient != 1:
            term += rf"\cdot{self.coefficient}"

        if self.addend != 0:
            term += f"+{self.addend}"

        return term

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return (
            self.exponent == other.exponent and
            self.coefficient == other.coefficient and
            self.addend == other.addend
        )

    def __lt__(self, other):
        if not isinstance(other, type(self)) or isinstance(other, int):
            return False

        return (
            self.exponent < other.exponent or
            self.coefficient < other.coefficient or
            self.addend < other.addend
        )

    def __gt__(self, other):
        if not isinstance(other, type(self)) or isinstance(other, int):
            return True

        return (
            self.exponent > other.exponent or
            self.coefficient > other.coefficient or
            self.addend > other.addend
        )

    def __add__(self, other):
        if isinstance(other, int) or self.exponent > other.exponent:
            return Ordinal(
                exponent=deepcopy(self.exponent),
                coefficient=deepcopy(self.coefficient),
                addend=self.addend + other,
            )

        elif self.exponent == other.exponent:

            if isinstance(self.addend, int):
                new_addend = deepcopy(other.addend)
            else:
                new_addend = self.addend + other.addend

            return Ordinal(
                exponent=deepcopy(self.exponent),
                coefficient=self.coefficient + other.coefficient,
                addend=new_addend,
            )

        return deepcopy(other)

    def __radd__(self, other):
        if isinstance(other, int):
            return deepcopy(self)
        raise NotImplemented

    def __mul__(self, other):
        return

    def __rmul__(self, other):
        return other * self

    def __pow__(self, other):
        return

    def __rpow__(self, other):
        return other ** self
