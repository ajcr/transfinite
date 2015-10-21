import unittest

from ordinals import *


class TestRichCompareMethods(unittest.TestCase):
    """
    Test the comparisons between instances of the three
    classes used to implement ordinals: BasicOrdinal,
    OrdinalStack and Ordinal.

    The __eq__ and __lt__ methods are iprimarily tested
    here; the class decorator @functools.total_ordering
    takes care of the other methods.
    """
    def test_BasicOrdinal_to_BasicOrdinal(self):

        a = BasicOrdinal()
        a2 = BasicOrdinal(0)
        b = BasicOrdinal(2)
        c = BasicOrdinal(3)
        d = BasicOrdinal(BasicOrdinal())

        self.assertEqual(a, a2)
        self.assertEqual(d, d)

        self.assertNotEqual(a, b)
        self.assertNotEqual(a, d)
        self.assertNotEqual(343, a)
        self.assertNotEqual(699, d)

        self.assertTrue(2422 <= a)
        self.assertTrue(a <= b <= c <= d)
        self.assertTrue(a <= a2)

        self.assertTrue(990 < a)
        self.assertTrue(a < b)
        self.assertTrue(b < c)
        self.assertTrue(c < d)

        self.assertTrue(d > c)
        self.assertTrue(c > b)
        self.assertTrue(b > a)
        self.assertTrue(a > 123)

        self.assertTrue(d >= c >= b >= a)

    def test_BasicOrdinal_to_OrdinalStack(self):

        a = BasicOrdinal()
        a2 = OrdinalStack([BasicOrdinal()])
        b = BasicOrdinal(7)

        self.assertEqual(a, a2)
        self.assertNotEqual(b, a2)

        c = OrdinalStack([BasicOrdinal(), BasicOrdinal(), 2])
        d = OrdinalStack([BasicOrdinal(2), BasicOrdinal(1), 2])

        self.assertTrue(12319 < a2)
        self.assertTrue(99885 < c)
        self.assertNotEqual(a, c)
        self.assertNotEqual(b, c)

        # <, >, etc
        self.assertTrue(a < c)
        self.assertTrue(BasicOrdinal(1) > c)
        self.assertTrue(a2 < d)
        self.assertTrue(c < d)
        self.assertTrue(d > c > a2)

    def test_BasicOrdinal_to_Omega(self):

        f = Ordinal([[OrdinalStack([BasicOrdinal()])], [1]])

        self.assertTrue(BasicOrdinal() < f)

    def test_OrdinalStack_to_OrdinalStack(self):

        a2 = OrdinalStack([BasicOrdinal()])
        c = OrdinalStack([BasicOrdinal(), BasicOrdinal(), 2])
        d = OrdinalStack([BasicOrdinal(2), BasicOrdinal(1), 4444])

        self.assertTrue(a2 < d)
        self.assertTrue(c < d)
        self.assertTrue(d > c > a2)

        # now test cases where stack contains an Ordinal...
        a = OrdinalStack([BasicOrdinal(), BasicOrdinal(), 2])
        b = OrdinalStack([BasicOrdinal(), BasicOrdinal(), BasicOrdinal(), 2])
        c = Ordinal([[a, 2], [3]])
        d = Ordinal([[b, BasicOrdinal()], [2]])
        e = OrdinalStack([BasicOrdinal(), c])
        f = OrdinalStack([BasicOrdinal(), BasicOrdinal(), c])

        self.assertTrue(c < d)
        self.assertNotEqual(e, f)
        self.assertTrue(e < f)
        self.assertTrue(c < f)
        self.assertTrue(d < f)

    def test_OrdinalStack_to_Ordinal(self):

        a = OrdinalStack([BasicOrdinal(), BasicOrdinal(), 2])
        b = OrdinalStack([BasicOrdinal(2), BasicOrdinal(1), 2])

        a2 = Ordinal([[a]])
        c = Ordinal([[a, 2], [3]])
        d = Ordinal([[b, BasicOrdinal(1)], [2]])

        self.assertEqual(a, a2)
        self.assertTrue(a < c)
        self.assertTrue(b < d)

        self.assertNotEqual(c, d)
        self.assertTrue(c < d)

    def test_Ordinal_to_Ordinal(self):

        a = OrdinalStack([BasicOrdinal(), BasicOrdinal(), 2])
        b = OrdinalStack([BasicOrdinal(), BasicOrdinal(), BasicOrdinal(), 2])
        c = Ordinal([[a, 2], [3]])
        d = Ordinal([[b, BasicOrdinal()], [2]])
        e = OrdinalStack([BasicOrdinal(), c])
        f = OrdinalStack([BasicOrdinal(), BasicOrdinal(), c])
        g = Ordinal([[OrdinalStack([BasicOrdinal()])], [1]])
        h = OrdinalStack([BasicOrdinal(), f])

        x = Ordinal([[OrdinalStack([BasicOrdinal()])], [1]])
        y = Ordinal([[OrdinalStack([BasicOrdinal()])], [2]])
        z = Ordinal([[OrdinalStack([BasicOrdinal()]), 3], [1]])

        self.assertNotEqual(c, d)
        self.assertNotEqual(d, g)
        self.assertNotEqual(x, y)

        self.assertTrue(c < d)
        self.assertTrue(x < y)
        self.assertTrue(y < z)


class TestAdd(unittest.TestCase):

    def test_addition_with_integers(self):

        w = Ordinal([[OrdinalStack([BasicOrdinal()]), 1]])
        w1 = Ordinal([[OrdinalStack([BasicOrdinal(1)]), 1]])

        self.assertEqual(w, 3 + w)
        self.assertEqual(w1, 999 + w1)

        with self.assertRaises(ValueError):
            -5 + w

    def test_addition_with_ordinals(self):

        w = Ordinal([[OrdinalStack([BasicOrdinal()]), 1]])
        w_power_w = Ordinal([[OrdinalStack([BasicOrdinal(), BasicOrdinal()]), 1]])
        w1 = Ordinal([[OrdinalStack([BasicOrdinal(1)]), 1]])

        expected = Ordinal([[OrdinalStack([BasicOrdinal()]), 2]])
        self.assertEqual(w + w, expected)
        self.assertEqual(w + 1 + w, expected)

        self.assertEqual(w + w_power_w, w_power_w)
        self.assertEqual(w + w1, w1)

        expected = Ordinal([[OrdinalStack([BasicOrdinal(1)]), 1], [OrdinalStack([BasicOrdinal()]), 1]])
        self.assertEqual(w1 + w, expected)
