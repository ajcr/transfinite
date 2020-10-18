from functools import total_ordering


def is_non_negative_int(n):
    return n >= 0 and isinstance(n, int)


@total_ordering
class Ordinal:
    """
    An infinite ordinal less than epsilon_0.

    This class describes an ordinal in Cantor Normal Form using
    the following attributes:

          (exponent)
         ^
        w . (coefficient) + (addend)

    Here (coefficient) is an integer, while (exponent) and (addend)
    can be either an integer or an instance of this Ordinal class.

    """

    def __init__(self, exponent=1, coefficient=1, addend=0):
        self.exponent = exponent
        self.coefficient = coefficient
        self.addend = addend

    def _repr_latex_(self):
        return rf"${self}$"

    def __repr__(self):
        term = "w"

        if self.exponent != 1:
            term += f"^({self.exponent})"
        if self.coefficient != 1:
            term += rf"*{self.coefficient}"
        if self.addend != 0:
            term += f" + {self.addend}"

        return term

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
            raise NotImplemented

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
            raise NotImplemented

    def __add__(self, other):
        try:
            if is_non_negative_int(other) or self.exponent > other.exponent:
                return self.__class__(
                    self.exponent, self.coefficient, self.addend + other
                )
        except AttributeError:
            raise NotImplemented
        if self.exponent == other.exponent:
            # if both addends are integers, new addend should not include self.addend
            if isinstance(self.addend, int):
                new_addend = other.addend
            else:
                new_addend = self.addend + other.addend
            return self.__class__(
                self.exponent,
                self.coefficient + other.coefficient,
                new_addend,
            )
        return other

    def __radd__(self, other):
        if is_non_negative_int(other):
            return self
        raise NotImplemented

    def __mul__(self, other):
        if other == 0:
            return 0
        if is_non_negative_int(other):
            return self.__class__(self.exponent, self.coefficient * other, self.addend)
        try:
            return self.__class__(
                self.exponent + other.exponent,
                other.coefficient,
                self.addend * other.addend + self * other.addend,
            )
        except AttributeError:
            raise NotImplemented

    def __rmul__(self, other):
        if other == 0:
            return 0
        if is_non_negative_int(other):
            return self.__class__(self.exponent, self.coefficient, other * self.addend)
        raise NotImplemented

    def __pow__(self, other):
        if other == 0:
            return 1
        if is_non_negative_int(other):
            return self.__class__(
                self.exponent * other, self.coefficient, self.addend * self
            )
        try:
            return self.__class__(self.exponent * other)
        except AttributeError:
            raise NotImplemented

    def __rpow__(self, other):
        if other == 0:
            return 0
        if is_non_negative_int(other):
            return self.__class__(
                self.exponent * self.coefficient, other ** self.addend
            )
        raise NotImplemented
