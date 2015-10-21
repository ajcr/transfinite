"""
Implementation of transfinite ordinals and ordinal arithmetic.

Best used in Jupyter/IPython so the LaTeX represention of the
ordinals can be properly rendered.
"""

import copy
from functools import total_ordering
from itertools import islice

def _hi_lo_bisect_right(lst, x):
    # bisect list sorted high -> low. Based on the code in:
    # https://hg.python.org/cpython/file/3.4/Lib/bisect.py
    hi, lo = 0, len(lst)
    while hi < lo:
        mid = (lo+hi) // 2
        if x > lst[mid]:
            lo = mid
        else:
            hi = mid + 1
    return hi


@total_ordering
class BasicOrdinal(object):
    """
    The building blocks of the Ordinal class.

    Represents limit ordinals of the form:

        \omega_{index}

    where index can be an integer or an instance of the
    BasicOrdinal, OrdinalStack or Ordinal classes.

    Contains general methods that the OrdinalStack class
    and Ordinal class will inherit.
    """

    cmp_error_string = "unorderable types: %s and %s"

    def __init__(self, index=0):
        self.index = index

    def __eq__(self, other):
        if type(other) is int:
            return False
        elif type(other) is BasicOrdinal:
            return self.index == other.index
        elif type(other) is OrdinalStack:
            return [self, 1] == other.stack
        elif type(other) is Ordinal:
            return [[self, 1]] == other.terms
        else:
            return False

    def __lt__(self, other):
        if type(other) is int:
            return False
        elif type(other) is BasicOrdinal:
            return self.index < other.index
        elif type(other) is OrdinalStack:
            return [self, 1] < other.stack
        elif type(other) is Ordinal:
            return [[self, 1]] < other.terms
        else:
            raise TypeError(self.cmp_error_string % (type(self), type(other)))

    def __str__(self):
        """
        LaTeX represention of the ordinal. If the index
        is 0, it is not included in the output following
        the convention that \omega == \omega_0.
        """
        if self.index:
            return "\omega_{%s}" % self.index
        else:
            return "\omega"

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


@total_ordering
class OrdinalStack(BasicOrdinal):
    """
    Used to represent exponentiation; one of the
    building blocks of the main Ordinal class.

    The last element in the stack is always an integer
    or an Ordinal instance.
    """
    def __init__(self, stack):
        self.stack = list(stack)
        if not isinstance(self.stack[-1], (int, Ordinal)):
            self.stack.append(1)
        self.index = self.stack[0].index

    @property
    def stack_contains_ordinal(self):
        return any(isinstance(x, Ordinal) for x in self.stack)

    def __str__(self):
        stk = self.stack
        if stk[-1] == 1:
            stk = stk[:-1]
        rbraces = '}'*(len(stk)-1)
        return '^{'.join([str(a) for a in stk]) + rbraces

    def __len__(self):
        return len(self.stack)

    # Notes on comparisons:
    #
    # If both stacks are free of Ordinals, we can simply compare the
    # .stack attribute of self and other lexicographically.
    #
    # However, if one of the two stacks contains an Ordinal instance 
    # this simple method could produce incorrect results. E.g. the 
    # comparison w^(w^(w)) < w^(w+1) would return True since we have 
    # that w < w+1.
    # 
    # Instead, we find out the position of the first Ordinal 
    # instance in the stacks and compare preceding elements in turn
    # (these will all be BasicOmega instances). If all of these initial 
    # values are equal, treat the remaining memeber of the stack as a
    # new OrdinalStack instance and compare it with the Ordinal.

    def __eq__(self, other):
        if type(other) is int:
            return False
        elif type(other) is BasicOrdinal:
            return self.stack == [other, 1]
        elif type(other) is OrdinalStack:
            return self.stack == other.stack # may need to refine this
        elif type(other) is Ordinal:
            return [[self]] == other.terms
        else:
            return False

    def __lt__(self, other):
        if type(other) is int:
            return False
        elif type(other) is BasicOrdinal:
            return self.stack < [other, 1]
        elif type(other) is OrdinalStack:
            if not self.stack_contains_ordinal and not other.stack_contains_ordinal:
                return self.stack < other.stack
            else:
                n = min(len(self), len(other))
                shortest = min((self, other), key=len)
                pairs = zip(self.stack, other.stack)
                for a, b in islice(pairs, n-1):
                    if a != b:
                        return a < b
                # ...now compare ordinal at top with rest of stack...
                if shortest is self:
                    return self.stack[-1] < OrdinalStack(other.stack[n-1:])
                else:
                    return OrdinalStack(self.stack[n-1:]) < other.stack[-1]
        elif type(other) is Ordinal:
            return [[self]] < other.terms
        else:
            raise TypeError(self.cmp_error_string % (type(self), type(other)))


@total_ordering
class Ordinal(BasicOrdinal):
    """
    Class for transfinite ordinals expressible using omega notation,
    represented in Cantor normal form.
    """
    def __init__(self, terms):
        # Internally Ordinal is just a list of lists, for example 
        # (w^w).2 + 1 is stored as [[OrdinalStack(w, w), 2], [1]]
        # where w is a BasicOrdinal instance.
        #
        # Each element of the list is a list of OrdinalStack
        # instances or integers, representing products. The last 
        # element in this list must be an integer.
        self.terms = terms
        self.index = self.terms[0][0].index
        self.is_successor = type(self.terms[-1][0]) is int
        self.is_limit = not self.is_successor

    @staticmethod
    def _make_product_string(trm):
        if len(trm) > 1 and trm[-1] == 1:
            return "\cdot".join([str(t) for t in trm[:-1]])
        else:
            return "\cdot".join([str(t) for t in trm])

    def __str__(self):
        products = [self._make_product_string(trm) for trm in self.terms]
        latex = " + ".join(products)
        return latex

    def __eq__(self, other):
        if type(other) is int:
            return False
        elif type(other) is BasicOrdinal:
            return self.terms == [[other]]
        elif type(other) is OrdinalStack:
            return self.terms == [[other]]
        elif type(other) is Ordinal:
            return self.terms == other.terms
        else:
            return False

    def __lt__(self, other):
        if type(other) is int:
            return False
        elif type(other) is BasicOrdinal:
            return self.terms < [[other]]
        elif type(other) is OrdinalStack:
            return self.terms < [[other]]
        elif type(other) is Ordinal:
            return self.terms < other.terms
        else:
            raise TypeError(self.cmp_error_string % (type(self), type(other)))

    def __add__(self, other):
        if type(other) is int:
            if other < 0:
                raise ValueError("can only add positive integers to ordinal")
            terms = self.terms[:]
            if self.is_successor:
                terms[-1][0] += other
            else:
                terms.append([other])
            return Ordinal(terms)

        # We can now assume other is an Ordinal and find out how 
        # many terms of self should "disappear". However we
        # cannot simply compare magnitudes as we need to allow
        # sums such as  w + w.2 == w.3 and w.5 + w == w.6.
        #
        # Therefore we need to strip the "multiples" of ordinals 
        # from each term first, find where to cut off self to 
        # insert other and then form the new list of terms.

        s_terms_no_mult = [term[:-1] for term in self.terms]
        o_lead_term_no_mult = other.terms[0][:-1]
        o_lead_term_mult = other.terms[0][-1]

        n = _hi_lo_bisect_right(s_terms_no_mult, o_lead_term_no_mult)

        if s_terms_no_mult[n-1] == o_lead_term_no_mult:
            s_last_term_mult = self.terms[n-1][-1]
            if type(s_last_term_mult) is int and type(o_lead_term_mult) is int:
                s_terms = copy.deepcopy(self.terms[:n])
                s_terms[n-1][-1] += o_lead_term_mult
                terms = s_terms + other.terms[1:]
            elif a < o_lead_term_mult:
                s_terms = copy.deepcopy(self.terms[:n-1])
                terms = s_terms + other.terms
            elif a > o_lead_term_mult:
                s_terms = copy.deepcopy(self.terms[:n])
                terms = s_terms + other.terms[1:]
        else:
            s_terms = self.terms[:n]
            o_terms = other.terms
            terms = s_terms + o_terms
        return Ordinal(terms)

    def __radd__(self, other):
        if type(other) is int and other > 0:
            return self
        else:
            raise ValueError("can only add ordinals and positive integers")

    def __mul__(self, other):
        if type(other) is int:
            if other < 0:
                raise ValueError("can only multiply positive integers with ordinal")
            lead_term = copy.deepcopy(self.terms[:1])
            lead_term[0][-1] *= other
            return Ordinal(lead_term + self.terms[1:])

        # and if other is not an integer...

    def __rmul__(self, other):
        if type(other) is int and other > 0:
            return self
        else:
            raise ValueError("can only multiply ordinals and positive integers")


def omega(index=0):
    return Ordinal([[OrdinalStack([BasicOrdinal(index)]), 1]])

w = omega
