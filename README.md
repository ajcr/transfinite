# transfinite

[![PyPI version](https://badge.fury.io/py/transfinite.svg)](https://badge.fury.io/py/transfinite)

Transfinite [ordinal arithmetic](https://en.wikipedia.org/wiki/Ordinal_arithmetic) and factorisation up to the first [epsilon number](https://en.wikipedia.org/wiki/Epsilon_numbers_(mathematics)).

## Installation

Works with Python 3. Can be installed via pip using:

```
pip install transfinite
```

## Usage

For a basic introduction to ordinal arithmetic, look at Wikipedia or see the notebook [here](https://github.com/ajcr/transfinite/blob/master/notebooks/ordinal_arithmetic_basics.ipynb).

Here's a quick demonstration of the library in Jupyter's qtconsole (note that the variable `w` is the first transfinite number). First, some ordinal arithmetic:

![alt tag](https://github.com/ajcr/transfinite/blob/master/images/transfinite_demo.png)

The Ordinal class implements several methods which can be used to check properties of the ordinal:

- `Ordinal.is_limit()`, returns True if the ordinal is a [limit ordinal](https://en.wikipedia.org/wiki/Limit_ordinal).
- `Ordinal.is_successor()`, returns True if the ordinal is a [successor ordinal](https://en.wikipedia.org/wiki/Successor_ordinal).
- `Ordinal.is_gamma()`, returns True if the ordinal is [additively indecomposable](https://en.wikipedia.org/wiki/Additively_indecomposable_ordinal).
- `Ordinal.is_delta()`, returns True if the ordinal is [multiplicatively indecomposable](https://en.wikipedia.org/wiki/Additively_indecomposable_ordinal#Multiplicatively_indecomposable).
- `Ordinal.is_prime()`, returns True if the ordinal is prime.

[Ordinal factorisation](https://en.wikipedia.org/wiki/Ordinal_arithmetic#Factorization_into_primes) into prime ordinals is also implemented. Any composite ordinal `a` can be written as a product of two or more prime ordinals less than `a`:

![alt tag](https://github.com/ajcr/transfinite/blob/master/images/transfinite_demo_2.png)

Note that finite ordinals are not factorised using this method.
