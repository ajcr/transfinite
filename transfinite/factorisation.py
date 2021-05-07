from transfinite.ordinal import Ordinal
from transfinite.ordinal_factors import OrdinalFactors
from transfinite.util import is_finite_ordinal, group_factors


def subtract(a, b):
    """
    Given ordinals a > b, return the ordinal c such that b + c == a

    """
    if a <= b:
        raise ValueError("First argument must be greater than second argument")

    if is_finite_ordinal(a):
        return a - b

    if is_finite_ordinal(b) or a.exponent > b.exponent:
        return a

    if a.exponent == b.exponent and a.coefficient == b.coefficient:
        return subtract(a.addend, b.addend)

    # Here we know that a.coefficient > b.coefficient
    return Ordinal(a.exponent, a.coefficient - b.coefficient, a.addend)


def divide_terms_by_ordinal(terms, ordinal):
    """
    Divide each term in the list by the specified ordinal.

    """
    return [Ordinal(subtract(t.exponent, ordinal.exponent), t.coefficient) for t in terms]


def ordinal_terms(ordinal):
    """
    Return a list containing all terms of the ordinal.

    For example:

      w**w**w + w**3 + w*7 + 9

    becomes the list

      [w**w**w, w**3, w*7, 9]

    """
    terms = []

    while not is_finite_ordinal(ordinal):
        term = Ordinal(exponent=ordinal.exponent, coefficient=ordinal.coefficient)
        terms.append(term)
        ordinal = ordinal.addend

    if ordinal:
        terms.append(ordinal)

    return terms


def factorise_term(term):
    """
    Write a single transfinite ordinal term (addend=0) as a product of primes.

    For example:

      w**(w**w*7 + w*3 + 2)

    becomes

      [(w**w**w, 7), (w**w, 3), (w, 2)]

    """
    factors_ = []

    for t in ordinal_terms(term.exponent):
        if is_finite_ordinal(t):
            factors_.append((Ordinal(), t))
        else:
            factors_.append((Ordinal(exponent=Ordinal(t.exponent)), t.coefficient))

    if term.coefficient > 1:
        factors_.append((term.coefficient, 1))

    return factors_


def factorise_term_successor(ordinal_term):
    """
    Given a term (w**e * c) return the factors of its successor.

    Note that since (w**e + 1) is prime, the method returns this
    ordinal as a factor, as well as the coefficient if not 1:

        term -> successor -> factors
        w    -> w + 1     -> [(w + 1, 1)]
        w*7  -> w*7 + 1   -> [(w + 1, 1), (7, 1)]

    """
    factors_ = [(Ordinal(exponent=ordinal_term.exponent, addend=1), 1)]

    if ordinal_term.coefficient > 1:
        factors_.append((ordinal_term.coefficient, 1))

    return factors_


def factors(ordinal):
    """
    Return the prime factors of the ordinal.

    Note: finite integers are not broken into prime factors.
    """
    terms = ordinal_terms(ordinal)

    # If the ordinal is a limit ordinal, it has the terms:
    #
    #   terms = A + B + ... + X    (A > B > ... > X > 0)
    #
    # We want to factor out X if X > 1, leaving:
    #
    #   terms = A' + B' + ... + 1  (X*A' == A, X*B' == B, ...)
    #
    # The factors of X are the first factors of the ordinal.
    # Note the finite term 1 is not explicitly included in the list.

    if len(terms) == 1 or not is_finite_ordinal(terms[-1]):
        least_term = terms.pop()
        terms = divide_terms_by_ordinal(terms, least_term)
        factors_ = factorise_term(least_term)

    elif terms[-1] > 1:
        factors_ = [(terms.pop(), 1)]

    else:
        terms.pop()
        factors_ = []

    # At this stage, terms is a list of infinite ordinals:
    #
    #   terms = A' + B' + ... + C'  (A' > B' > C' >= w)
    #
    # This represents the successor ordinal:
    #
    #   A' + B' + ... + C' + 1
    #
    # The loop below repeatedly removes the least term C' then adds
    # factors of (C' + 1) to the list of factors, then divides C'
    # into the remaining terms (A', B', ...).

    while terms:
        least_term = terms.pop()
        factors_ += factorise_term_successor(least_term)
        terms = divide_terms_by_ordinal(terms, least_term)

    return OrdinalFactors(group_factors(factors_))
