from transfinite.ordinal import Ordinal
from transfinite.util import is_finite_ordinal


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
    return Ordinal(
        exponent=a.exponent, coefficient=a.coefficient - b.coefficient, addend=a.addend
    )


def ordinal_terms(a):
    """
    Return a list containing all terms of the ordinal.

    For example:

      w**w**w + w**3 + w*7 + 9

    becomes the list

      [w**w**w, w**3, w*7, 9]

    """
    terms = []

    while not is_finite_ordinal(a):
        t = Ordinal(exponent=a.exponent, coefficient=a.coefficient)
        terms.append(t)
        a = a.addend

    if a:
        terms.append(a)

    return terms


def factorise_term(term):
    """
    Write a single transfinite ordinal term (addend=0) as a product of primes.

    For example:

      w**(w**w*7 + w*3 + 2)

    becomes

      [(w**w**w, 7), (w**w, 3), (w, 2)]

    """
    fs = []

    for t in ordinal_terms(term.exponent):
        if is_finite_ordinal(t):
            fs.append((Ordinal(), t))
        else:
            fs.append((Ordinal(exponent=Ordinal(t.exponent)), t.coefficient))

    if term.coefficient > 1:
        fs.append((term.coefficient, 1))

    return fs


def factorise_term_successor(ordinal_term):
    """
    Given a term (w**e * c) return the factors of its successor.

    Note that since (w**e + 1) is prime, the method returns this
    ordinal as a factor, as well as the coefficient if not 1.
    """
    fs = [(Ordinal(exponent=ordinal_term.exponent, addend=1), 1)]

    if ordinal_term.coefficient > 1:
        fs.append((ordinal_term.coefficient, 1))

    return fs


def factors(ordinal):
    """
    Return the prime factors of the ordinal.

    The factors are returned as a list of the form:

      [(factor_1, exponent_1), (factor_2, exponent_2), ...]

    Note: finite integers are not broken into prime factors.
    """
    if is_finite_ordinal(ordinal) or ordinal.is_prime():
        return [(ordinal, 1)]

    terms = ordinal_terms(ordinal)

    if len(terms) == 1:
        return factorise_term(terms[0])

    fs = factorise_term(terms.pop()) if ordinal.is_limit() else [(terms.pop(), 1)]

    # At this stage, terms is a list of infinite ordinals ordered from largest
    # to smallest. The loop below removes least term and adds the factors of its
    # successor to the list of factors, then divides it into the remaining terms.

    while terms:

        *terms, least_term = terms

        fs += factorise_term_successor(least_term)

        terms = [
            Ordinal(
                exponent=subtract(t.exponent, least_term.exponent),
                coefficient=t.coefficient,
            )
            for t in terms
        ]

    return fs
