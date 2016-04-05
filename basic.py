from functools import total_ordering


@total_ordering
class BasicOrdinal(object):
    """
    Represents limit ordinals of the form:

        \omega_{index}

    where index can be an integer or an instance of the
    BasicOrdinal, OrdinalStack or Ordinal classes.

    Contains general methods that the OrdinalStack class
    and Ordinal class will inherit.

    Must compare strictly greater than any int object.
    """

    _cmp_error_string = 'unorderable types: %s and %s'

    def __init__(self, index=0):
        self.index = index

    def __eq__(self, other):
        if isinstance(other, int):
            return False
        elif type(other) is BasicOrdinal:
            return self.index == other.index
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, int):
            return False
        elif type(other) is BasicOrdinal:
            return self.index < other.index
        else:
            raise TypeError(self._cmp_error_string % (type(self), type(other)))

    def __str__(self):
        """
        LaTeX represention of the ordinal. If the index
        is 0 (i.e. this is the first countably infinite
        ordinal), it is not included in the output.
        """
        if self.index:
            return '\omega_{%s}' % self.index
        else:
            return '\omega'

    def __repr__(self):
        return str(self)

    def _repr_latex_(self):
        return r"$%s$" % str(self)

    @property
    def is_countable(self):
        return self.index == 0

    @property
    def is_uncountable(self):
        return self.index > 0
