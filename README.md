# transfinite

`transfinite` introduces transfinite ordinals below epsilon_0 to Python.

These ordinal objects interact naturally with Python's integers (finite ordinals) and support ordinal arithmetic operations (addition, multiplication and exponentiation).

In Jupyter notebooks, ordinals are printed in LaTeX for easy interpretation.

## Installation

Works with Python 3. Use of the Jupyter/IPython notebook/qtconsole is highly recommended, but not mandatory:

```
pip install transfinite
```

To install from git, set up a virtualenv (optional), clone the repository (e.g. `git clone https://github.com/ajcr/transfinite.git`), navigate to the new directory and run `python -m pip install -e .`.

Tests can be run by invoking `pytest`.

## Usage

For a very basic introduction to ordinal arithmetic, look at the notebook [here](https://github.com/ajcr/transfinite/blob/master/notebooks/ordinal_arithmetic_basics.ipynb).

Here's a quick demonstration showing arithmetic with the first transfinite ordinal, omega (denoted as `w`):

![alt tag](https://github.com/ajcr/transfinite/blob/master/images/transfinite_demo.png)
