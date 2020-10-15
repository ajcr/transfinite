from functools import total_ordering
from typing import List


def _term_as_latex_string(ordinal):
    exponent_tower = []
    while ordinal.exponent != 1:
        exponent_tower.append(())
        ordinal = ordinal.exponent
    return


def is_less_than(left, right) -> bool:

    if isinstance(left, int) and isinstance(right, int):
        return left < right

    elif isinstance(left, int):
        return True

    elif isinstance(right, int):
        return False

    return left < right


def is_equal_to(left, right) -> bool:

    if isinstance(left, int) and isinstance(right, int):
        return left == right

    elif isinstance(left, int):
        return False

    elif isinstance(right, int):
        return False

    return left == right


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


def as_latex_string(ordinal) -> str:
    if isinstance(ordinal, int):
        return str(ordinal) 

    exp = as_latex_string(ordinal.exponent)
    coeff = as_latex_string(ordinal.coefficient)
    add = as_latex_string(ordinal.addend)

    return rf"\omega^{{{exp}}} \cdot {coeff} + {add}"


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
            #copy.deepcopy(self.exponent),
            self.exponent,
            self.coefficient,
        )

    def __repr__(self):
        return str(self)

    def _repr_latex_(self):
        return rf"${self}$"

    def __str__(self):
        return as_latex_string(self)

    def __eq__(self, other):

        if not isinstance(other, type(self)):
            return False

        return (
            is_equal_to(self.exponent, other.exponent) and
            is_equal_to(self.coefficient, other.coefficient) and
            is_equal_to(self.addend, other.addend)
        )

    def __lt__(self, other):

        if not isinstance(other, type(self)):
            return False

        if isinstance(other, int):
            return False

        return (
            is_less_than(self.exponent, other.exponent) or
            is_less_than(self.coefficient, other.coefficient) or
            is_less_than(self.addend, other.addend)
        )

    def __add__(self, other):
        if isinstance(other, int):
            return add_finite_integer(self, other)

        head = self

        while head.exponent != other:
            return head

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


w = Ordinal()
