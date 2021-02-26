# transfinite

[![PyPI version](https://badge.fury.io/py/transfinite.svg)](https://badge.fury.io/py/transfinite)

Transfinite [ordinal arithmetic](https://en.wikipedia.org/wiki/Ordinal_arithmetic) and factorisation up to the first [epsilon number](https://en.wikipedia.org/wiki/Epsilon_numbers_(mathematics)).

## Installation

Works with Python 3, just install with:

```
pip install transfinite
```

## Usage

For a very basic introduction to ordinal arithmetic, look at Wikipedia or see the notebook [here](https://github.com/ajcr/transfinite/blob/master/notebooks/ordinal_arithmetic_basics.ipynb).

Here's a quick demonstration in Jupyter's qtconsole (note that the variable `w` is the first transfinite number). First, some ordinal arithmetic:

![alt tag](https://github.com/ajcr/transfinite/blob/master/images/transfinite_demo.png)

Ordinal factorisation is also implemented. Any composite ordinal can be written as a product of prime ordinals:

![alt tag](https://github.com/ajcr/transfinite/blob/master/images/transfinite_demo_2.png)

The Ordinal class implements an `is_prime()` method which will indicate if the ordinal object is prime or not.
