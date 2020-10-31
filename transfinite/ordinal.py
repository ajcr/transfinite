from functools import total_ordering


def is_non_negative_int(n):
    """
    Return True if n is a non-negative integer.

    If n is a negative integer raise a ValueError, else return False.
    """
    if isinstance(n, int) and n >= 0:
        return True
    if isinstance(n, int):
        raise ValueError(f"int value must be non-negative (got {n})")
    return False


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

        if not isinstance(exponent, (int, Ordinal)):
            raise TypeError("exponent must be an Ordinal or an integer greater than 0")

        if exponent < 1:
            raise ValueError("exponent must be an Ordinal or an integer greater than 0")

        if not isinstance(coefficient, int):
            raise TypeError("coefficient must be an integer greater than 0")

        if coefficient < 1:
            raise ValueError("coefficient must be an integer greater than 0")

        if not isinstance(addend, (int, Ordinal)):
            raise TypeError("addend must be an Ordinal or a non-negative integer")

        if isinstance(addend, int) and addend < 0:
            raise ValueError("addend must be an Ordinal or a non-negative integer")

        if isinstance(addend, Ordinal) and addend.exponent >= exponent:
            raise ValueError(f"addend.exponent must be less than exponent {exponent}")

        self.exponent = exponent
        self.coefficient = coefficient
        self.addend = addend

    def is_limit(self):
        if is_non_negative_int(self.addend):
            return self.addend == 0
        return self.addend.is_limit()

    def is_successor(self):
        return not self.is_limit()

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
            is_non_negative_int(self.exponent)
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
                # smaller exponent on leading term
                self.exponent < other.exponent
                # or equal exponent on leading term and smaller coefficient
                or self.exponent == other.exponent
                and self.coefficient < other.coefficient
                # or equal leading term and smaller addend
                or self.exponent == other.exponent
                and self.coefficient == other.coefficient
                and self.addend < other.addend
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
        if other in (0, 1):
            return other
        if self.exponent == 1:
            return Ordinal(self.coefficient, other ** self.addend)
        # n**w**k == n**w**(k - 1) for all 1 < n,k < w
        if is_non_negative_int(self.exponent):
            return Ordinal(
                Ordinal((self.exponent - 1) * self.coefficient, other ** self.addend)
            )
        # n**w**a == w**w**a for all 1 < n < w and a >= w
        return Ordinal(Ordinal(self.exponent, self.coefficient)) * other ** self.addend
