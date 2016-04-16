"""
Implementation of transfinite ordinals and ordinal arithmetic.

Best used in Jupyter/IPython so the LaTeX represention of the
ordinals can be properly rendered.

Notes on classes: the BasicOrdinal and OrdinalStack classes are
used to build up and represent ordinals (in the Ordinal class).
These are internal classes and should not be called by the user
directly.

"""

import copy
from functools import total_ordering
from itertools import islice
import operator

from algorithms import hi_lo_bisect_right, product
from basic import BasicOrdinal


@total_ordering
class OrdinalStack(BasicOrdinal):
    """
    Represents ordinal exponentiation; one of the
    building blocks of the Ordinal class.

    Internally, self.stack is a list of BasicOrdinal,
    Ordinal and integer instances.

    The last element is always an integer or an
    Ordinal instance.
    """
    def __init__(self, stack):
        self.stack = stack
        self.index = self.stack[0].index

    @property
    def stack_contains_ordinal(self):
        return any(isinstance(x, Ordinal) for x in self.stack)

    def __str__(self):
        # if the element at the top of the stack
        # is 1, we don't print this element.
        stk = self.stack
        if stk[-1] == 1:
            stk = stk[:-1]
        rbraces = '}'*(len(stk)-1)
        return '^{'.join([str(a) for a in stk]) + rbraces

    def __len__(self):
        return len(self.stack)

    # Notes on comparison:
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
    # (these will all be BasicOrdinal instances). If all of these initial 
    # values are equal, treat the remaining memeber of the stack as a
    # new OrdinalStack instance and compare it with the Ordinal.

    def _compare_op(self, other, op):
        try:
            if not self.stack_contains_ordinal and not other.stack_contains_ordinal:
                return op(self.stack, other.stack)
            else:
                n = min(len(self), len(other))
                shortest = min((self, other), key=len)
                pairs = zip(self.stack, other.stack)
                for a, b in islice(pairs, n-1):
                    if a != b:
                        return op(a, b)
                # ...now compare ordinal at top with rest of stack...
                if n == len(self) == len(other):
                    return op(self.stack[-1], other.stack[-1])
                elif shortest is self:
                    return op(self.stack[-1], self.__class__(other.stack[n-1:]))
                else:
                    return op(self.__class__(self.stack[n-1:]), other.stack[-1])
        except AttributeError:
            # assumes other is an instance of Ordinal class 
            return op([[self, 1]], other.terms)

    def __lt__(self, other):
        return self._compare_op(other, operator.lt)

    def __eq__(self, other):
        return self._compare_op(other, operator.eq)

    # this function should be re-written; it repeats itself a lot
    @staticmethod
    def add_stack_powers(a, b):
        """
        If two OrdinalStack instances a and b have
        the same base (index 0 of the stack) then
        return a new OrdinalStack instance with
        the powers added together.
        """
        base = a.stack[0]
        a_power = a.stack[1:]
        b_power = b.stack[1:]

        if isinstance(a_power[0], int):
            if isinstance(b_power[0], int):
                return OrdinalStack([base, a_power[0] + b_power[0]]) # 1
            elif isinstance(b_power[0], Ordinal):
                return OrdinalStack([base, b_power[0]])
            else:
                power = Ordinal([[OrdinalStack(b_power), 1]])
                return OrdinalStack([base, power])

        elif isinstance(a_power[0], Ordinal):
            if isinstance(b_power[0], int):
                return OrdinalStack([base, a_power[0] + b_power[0]]) # 1
            elif isinstance(b_power[0], Ordinal):
                return OrdinalStack([base, a_power[0] + b_power[0]]) # 1
            else:
                power = a_power[0] + Ordinal([[OrdinalStack(b_power), 1]])
                return OrdinalStack([base, power])

        else:
            a = Ordinal([[OrdinalStack(a_power), 1]])
            if isinstance(b_power[0], int):
                power = a + b_power[0]
                return OrdinalStack([base, power])
            elif isinstance(b_power[0], Ordinal):
                power = a + b_power[0]
                return OrdinalStack([base, power])
            else:
                b = Ordinal([[OrdinalStack(b_power), 1]])
                return OrdinalStack([base, a + b])

    def multiply_stack_power_by_ordinal(self, other):
        """
        Treat self.stack[1:] as an Ordinal and multiply
        it by the Ordinal other. Return a new instance
        with self.stack[1:] equal to the new Ordinal.
        """
        base = self.stack[0]
        self_power = self.stack[1:]
        if isinstance(self_power[0], int):
            return OrdinalStack([base, other])
        else:
            if isinstance(self_power[0], Ordinal):
                power = self_power[0] * other
            else:
                power = Ordinal([[self.__class__(self_power), 1]]) * other
            return self.__class__([base, power])


@total_ordering
class Ordinal(BasicOrdinal):
    """
    Represents transfinite ordinals in Cantor normal form.

    Internally, this class is just a list of lists (known
    as "terms"). Each sublist is itself a list of
    OrdinalStack instances and/or integers. For example,
    the ordinal (w^w).2 + 1 is stored as

        [[OrdinalStack(w, w), 2], [1]]

    The last element in each sublist is always the integer
    1 (this is to ensure the arithemtic methods work).

    Use an appropriate classmethod (e.g. from_index) to
    intitalise instances of this class, rather than calling
    the __init__ method directly.
    """
    def __init__(self, terms):
        self.terms = terms
        self.index = self.terms[0][0].index

    @property
    def is_successor(self):
        return isinstance(self.terms[-1][0], int)

    @property
    def is_limit(self):
        return not self.is_successor

    @classmethod
    def from_index(cls, index=0):
        """
        Constructs Ordinals of the form:

            \omega_{index}

        where index can be an integer or another ordinal.
        """
        if not isinstance(index, (int, Ordinal)):
            raise TypeError("index must be an integer or an Ordinal instance")
        return cls([[OrdinalStack([BasicOrdinal(index), 1]), 1]])

    @staticmethod
    def _make_product_string(trm):
        if len(trm) > 1 and trm[-1] == 1:
            # don't print 1 if we just have one copy
            return "\cdot".join([str(t) for t in trm[:-1]])
        else:
            return "\cdot".join([str(t) for t in trm])

    def __str__(self):
        products = [self._make_product_string(trm) for trm in self.terms]
        return ' + '.join(products)

    def __eq__(self, other):
        if type(other) is int:
            return False
        elif type(other) is OrdinalStack:
            return self.terms == [[other, 1]]
        elif type(other) is Ordinal:
            return self.terms == other.terms
        else:
            return False

    def __lt__(self, other):
        if type(other) is int:
            return False
        elif type(other) is OrdinalStack:
            return self.terms < [[other, 1]]
        elif type(other) is Ordinal:
            return self.terms < other.terms
        else:
            raise TypeError(self._cmp_error_string % (type(self), type(other)))

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
        else:
            s_terms_no_mult = [term[:-1] for term in self.terms]
            o_lead_term_no_mult = other.terms[0][:-1]
            o_lead_term_mult = other.terms[0][-1]

            n = hi_lo_bisect_right(s_terms_no_mult, o_lead_term_no_mult)

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

    def _multiply_by_integer(self, n):
        lead_term = copy.deepcopy(self.terms[:1])
        lead_term[0][-1] *= n
        return Ordinal(lead_term + self.terms[1:])

    def __mul__(self, other):
        if isinstance(other, int):
            if other < 0:
                raise ValueError("can only multiply ordinals and positive integers")
            elif other == 0:
                return 0
            else:
                terms = self._multiply_by_integer(other)
                return Ordinal(terms.terms)
        else:
            s_lead_term = self.terms[0]
            terms = []
            indexes = [getattr(x, 'index', -1) for x in s_lead_term]
            for o_term in other.terms:
                try:
                    n = hi_lo_bisect_right(indexes, o_term[0].index)
                    if indexes[n-1] == o_term[0].index:
                        new_stack = OrdinalStack.add_stack_powers(s_lead_term[n-1], o_term[0])
                        term = s_lead_term[:n-1] + [new_stack] + o_term[1:]
                    else:
                        term = s_lead_term[:n] + o_term
                    terms.append(term)
                except AttributeError:
                    # no .index attribute so we have an integer
                    term = self._multiply_by_integer(o_term[0])
                    terms.extend(term.terms)
            return Ordinal(terms)

    def __rmul__(self, other):
        if type(other) is int and other > 0:
            return self
        else:
            raise ValueError("can only multiply ordinals and positive integers")

    def _raise_to_integer_power(self, n):
        # naive approach: repeated multiplication (this 
        # does not scale well).

        # TODO: find a formula for finite powers of ordinals.
        return product(self for _ in range(n))

    def _raise_ordinal_to_single_term_power(self, other):
        if self.index < other.index:
            return other._raise_lower_index_to_single_term_power()
        else:
            lead_term = self.terms[0][0]
            other_terms = self.terms[0][1:]
            new_lead_term = lead_term.multiply_stack_power_by_ordinal(other)
            terms = [[new_lead_term, 1]]
            return Ordinal(terms)

    def _raise_lower_index_to_single_term_power(self):
        lead_term = self.terms[0][0]
        tail_terms = self.terms[0][1:]
        idx = lead_term.index
        if lead_term.stack[1] == 1:
            ret = self.from_index(idx)
        elif isinstance(lead_term.stack[1], int):
            n = lead_term.stack[1] - 1
            base = BasicOrdinal(idx)
            stk = OrdinalStack([base, base, n])
            ret = Ordinal([[stk, 1]])
        else:
            base = BasicOrdinal(idx)
            stk = OrdinalStack([base] + lead_term.stack)
            ret = Ordinal([[stk, 1]])

        # finally, raise ret Ordinal to power of tail_terms
        if isinstance(tail_terms[0], int):
            a = tail_terms[0]
            return ret._raise_to_integer_power(a)
        else:
            a = Ordinal([tail_terms])
            return ret._raise_ordinal_to_single_term_power(a)

    def __pow__(self, other):
        if isinstance(other, int):
            if other > 0:
                return self._raise_to_integer_power(other)
            elif other == 0:
                return 1
            else:
                raise ValueError("Cannot raise Ordinal to negative integer power")
        else:
            ordinals = []
            for term in other.terms:
                if len(term) > 1:
                    a = Ordinal([term])
                    b = self._raise_ordinal_to_single_term_power(a)
                else:
                    a = term[0]
                    b = self._raise_to_integer_power(a)
                ordinals.append(b)
            return product(ordinals)

    def __rpow__(self, other):
        if other == 1 or other == 0:
            return other
        elif isinstance(other, int) and other < 0:
            raise ValueError("Cannot raise negative integer to Ordinal power")
        else:
            ordinals = []
            for term in self.terms:
                if len(term) > 1:
                    a = Ordinal([term])
                    b = self._raise_lower_index_to_single_term_power()
                else:
                    a = term[0]
                    b = other ** a
                ordinals.append(b)
            return product(ordinals)

