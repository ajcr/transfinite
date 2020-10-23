from functools import total_ordering


def is_non_negative_int(n):
    return isinstance(n, int) and n >= 0


def exp_by_squaring(x, n):
    if n == 0:
        return 1
    if n == 1:
        return x
    if n % 2 == 0:
        return exp_by_squaring(x * x, n // 2)
    return exp_by_squaring(x * x, (n - 1) // 2) * x


def as_latex(ordinal):
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
        self.exponent = exponent
        self.coefficient = coefficient
        self.addend = addend

    def _repr_latex_(self):
        return f"${as_latex(self)}$"

    def __repr__(self):
        return str(self)

    def __str__(self):
        term = "w"
        if self.exponent != 1:
            term += f"**({self.exponent})"
        if self.coefficient != 1:
            term += f"*{self.coefficient}"
        if self.addend != 0:
            term += f"+{self.addend}"
        return term

    def __eq__(self, other):
        try:
            return (
                self.exponent == other.exponent
                and self.coefficient == other.coefficient
                and self.addend == other.addend
            )
        except AttributeError:
            return False

    def __lt__(self, other):
        if is_non_negative_int(other):
            return False
        try:
            return (
                self.exponent < other.exponent
                or self.coefficient < other.coefficient
                or self.addend < other.addend
            )
        except AttributeError:
            return NotImplemented

    def __gt__(self, other):
        if is_non_negative_int(other):
            return True
        try:
            return (
                self.exponent > other.exponent
                or self.coefficient > other.coefficient
                or self.addend > other.addend
            )
        except AttributeError:
            return NotImplemented

    def __add__(self, other):
        try:
            if is_non_negative_int(other) or self.exponent > other.exponent:
                return Ordinal(self.exponent, self.coefficient, self.addend + other)
        except AttributeError:
            return NotImplemented
        if self.exponent == other.exponent:
            return Ordinal(
                self.exponent, self.coefficient + other.coefficient, other.addend
            )
        return other

    def __radd__(self, other):
        if not is_non_negative_int(other):
            return NotImplemented
        return self

    def __mul__(self, other):
        if is_non_negative_int(other):
            return other and Ordinal(
                self.exponent, self.coefficient * other, self.addend
            )
        try:
            return Ordinal(
                self.exponent + other.exponent,
                other.coefficient,
                self.addend * other.addend + self * other.addend,
            )
        except AttributeError:
            return NotImplemented

    def __rmul__(self, other):
        if not is_non_negative_int(other):
            return NotImplemented
        return other and Ordinal(self.exponent, self.coefficient, other * self.addend)

    def __pow__(self, other):
        if is_non_negative_int(other):
            return exp_by_squaring(self, other)
        try:
            return (
                Ordinal(self.exponent * Ordinal(other.exponent, other.coefficient))
                * self ** other.addend
            )
        except AttributeError:
            return NotImplemented

    def __rpow__(self, other):
        if not is_non_negative_int(other):
            return NotImplemented
        if other == 0:
            return 0
        if self.exponent == 1:
            return Ordinal(self.coefficient, other ** self.addend)
        if is_non_negative_int(self.exponent):
            return Ordinal(
                Ordinal((self.exponent - 1) * self.coefficient, other ** self.addend)
            )
        return Ordinal(Ordinal(self.exponent, self.coefficient)) * other ** self.addend
