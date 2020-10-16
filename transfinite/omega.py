from functools import total_ordering
from typing import List


def as_cnf_terms(ordinal) -> List:
    """
    Return a list of terms for the ordinal:

      w^w + w^7 + 3 -> [w^w, w^7, 3]
      w.2 + 5       -> [w.2, 5]

    """
    terms = [ordinal.head()]
    
    while ordinal.addend != 0:
        try:
            ordinal = ordinal.addend
        except AttributeError:
            terms.append(ordinal)
            break
        terms.append(ordinal.head())

    return terms

def as_exponent_terms(ordinal) -> List:
    """
    Return a list of terms for the exponent tower:

      w^w^(w+1)     -> [w, w, w+1]
      w^w^(w^2 + 1) -> [w, w, w^2 + 1]

    Note that any addend of the ordinal is ignored.
    """
    terms = [ordinal.coeffient]
    exponent = ordinal.exponent
    
    while True:
        exponent = exponent.exponent
        if isinstance(ordinal, int):
            terms.append(ordinal.exponent)
            break
        terms.append(ordinal.head())

    return terms


@total_ordering
class Ordinal:
    r"""
    An ordinal less than \epsilon_0 in CNF.

    """
    def __init__(self, exponent=1, coefficient=1, addend=0):
        self.exponent = exponent
        self.coefficient = coefficient
        self.addend = addend
        
    def head(self):
        return self.__class__(
            self.exponent,
            self.coefficient,
        )

    def __repr__(self):
        return str(self)

    def _repr_latex_(self):
        return rf"${self}$"

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
        return

    def __radd__(self, other):
        return other + self

    def __mul__(self, other):
        return

    def __rmul__(self, other):
        return other * self

    def __pow__(self, other):
        return

    def __rpow__(self, other):
        return other ** self
