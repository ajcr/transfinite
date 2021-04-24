from functools import total_ordering

from transfinite.util import is_finite_ordinal, as_latex, exp_by_squaring


class OrdinalConstructionError(Exception):
    pass


@total_ordering
class Ordinal:
    """
    An infinite ordinal less than epsilon_0.

    This class describes an ordinal in Cantor Normal Form using
    the following attributes:

          (exponent)
         ^
        w . (coefficient) + (addend)

    w denotes the first infinite ordinal, (coefficient) is an integer,
    (exponent) and (addend) can be either an integer or an instance of
    this Ordinal class.

    """

    def __init__(self, exponent=1, coefficient=1, addend=0):

        if exponent == 0 or not is_ordinal(exponent):
            raise OrdinalConstructionError("exponent must be an Ordinal or an integer greater than 0")

        if coefficient == 0 or not is_finite_ordinal(coefficient):
            raise OrdinalConstructionError("coefficient must be an integer greater than 0")

        if not is_ordinal(addend):
            raise OrdinalConstructionError("addend must be an Ordinal or a non-negative integer")

        if isinstance(addend, Ordinal) and addend.exponent >= exponent:
            raise OrdinalConstructionError("addend.exponent must be less than self.exponent")

        self.exponent = exponent
        self.coefficient = coefficient
        self.addend = addend

    def is_limit(self):
        """
        Return true if ordinal is a limit ordinal.

        """
        if is_finite_ordinal(self.addend):
            return self.addend == 0
        return self.addend.is_limit()

    def is_successor(self):
        """
        Return true if ordinal is a successor ordinal.

        """
        return not self.is_limit()

    def is_gamma(self):
        """
        Return true if ordinal is addititively indecomposable.

        These are ordinals of the form  w**a  for a > 0.
        """
        return self.coefficient == 1 and self.addend == 0

    def is_delta(self):
        """
        Return true if ordinal is multiplicatively indecomposable.

        These are ordinals of the form  w**w**a  for an ordinal a
        which is either 0 or such that w**a is a gamma ordinal.
        """
        return self.is_gamma() and (
            self.exponent == 1
            or not is_finite_ordinal(self.exponent)
            and self.exponent.is_gamma()
        )

    def is_prime(self):
        """
        Return true if ordinal cannot be factored into smaller ordinals,
        both greater than 1:

         * ordinal is the successor of a gamma ordinal, or
         * ordinal is a delta ordinal

        """
        return self.coefficient == 1 and self.addend == 1 or self.is_delta()

    def _repr_latex_(self):
        return f"${as_latex(self)}$"

    def __repr__(self):
        return str(self)

    def __str__(self):
        term = "w"

        # Only use parentheses for exponent if finite and greater than 1,
        # or its addend is nonzero or its coefficient is greater than 1.

        if self.exponent == 1:
            pass

        elif (
            is_finite_ordinal(self.exponent)
            or self.exponent.coefficient == 1
            and self.exponent.addend == 0
        ):
            term += f"**{self.exponent}"

        else:
            term += f"**({self.exponent})"

        if self.coefficient != 1:
            term += f"*{self.coefficient}"

        if self.addend != 0:
            term += f" + {self.addend}"

        return term

    def __hash__(self):
        return hash((hash(self.exponent), hash(self.coefficient), hash(self.addend)))

    def __eq__(self, other):
        if isinstance(other, Ordinal):
            return self.as_tuple() == other.as_tuple()
        return False

    def __lt__(self, other):
        if isinstance(other, Ordinal):
            return self.as_tuple() < other.as_tuple()
        if is_finite_ordinal(other):
            return False
        return NotImplemented

    def __add__(self, other):

        if not is_ordinal(other):
            return NotImplemented

        # (w**a*b + c) + x == w**a*b + (c + x)
        if is_finite_ordinal(other) or self.exponent > other.exponent:
            return Ordinal(self.exponent, self.coefficient, self.addend + other)

        # (w**a*b + c) + (w**a*d + e) == w**a*(b + d) + e
        if self.exponent == other.exponent:
            return Ordinal(self.exponent, self.coefficient + other.coefficient, other.addend)

        # other is strictly greater than self
        return other

    def __radd__(self, other):

        if not is_finite_ordinal(other):
            return NotImplemented

        # n + a == a
        return self

    def __mul__(self, other):

        if not is_ordinal(other):
            return NotImplemented

        if other == 0:
            return 0

        # (w**a*b + c) * n == w**a * (b*n) + c
        if is_finite_ordinal(other):
            return Ordinal(self.exponent, self.coefficient * other, self.addend)

        # (w**a*b + c) * (w**x*y + z) == w**(a + x)*y + (c*z + (w**a*b + c)*z)
        return Ordinal(
            self.exponent + other.exponent,
            other.coefficient,
            self.addend * other.addend + self * other.addend,
        )

    def __rmul__(self, other):

        if not is_finite_ordinal(other):
            return NotImplemented

        if other == 0:
            return 0

        # n * (w**a*b + c) == w**a*b + (n*c)
        return Ordinal(self.exponent, self.coefficient, other * self.addend)

    def __pow__(self, other):

        if not is_ordinal(other):
            return NotImplemented

        # Finite powers are computed using repeated multiplication
        if is_finite_ordinal(other):
            return exp_by_squaring(self, other)

        # (w**a*b + c) ** (w**x*y + z) == (w**(a * w**x * y)) * (w**a*b + c)**z
        return Ordinal(self.exponent * Ordinal(other.exponent, other.coefficient)) * self**other.addend

    def __rpow__(self, other):

        if not is_finite_ordinal(other):
            return NotImplemented

        # 0**a == 0 and 1**a == 1
        if other in (0, 1):
            return other

        # n**(w*c + a) == (w**c) * (n**a)
        if self.exponent == 1:
            return Ordinal(self.coefficient, other ** self.addend)

        # n**(w**m*c + a) == w**(w**(m-1) * c) * n**a
        if is_finite_ordinal(self.exponent):
            return Ordinal(Ordinal(self.exponent - 1, self.coefficient)) * other**self.addend

        # n**(w**a*c + b) == w**(w**a*c) * n**b
        return Ordinal(Ordinal(self.exponent, self.coefficient)) * other**self.addend

    def as_tuple(self):
        """
        Return the ordinal as a tuple of (exponent, coefficient, addend).

        """
        return self.exponent, self.coefficient, self.addend


def is_ordinal(a):
    """
    Return True if a is a finite or infinite ordinal.

    """
    return is_finite_ordinal(a) or isinstance(a, Ordinal)
