# py-omega

Learn transfinite ordinal arithmetic in Python.

Construct transfinite ordinals, then compare and combine them using addition, multiplication and exponentiation.

## Overview

Works with Python 3.2 and higher. Use a Jupyter/IPython notebook/qtconsole to have the LaTeX output properly rendered.

```python
from pyomega import *
```

Here's a quick demonstration...

Create initial ordinals with the `omega` function:

![alt tag](https://github.com/ajcr/py-omega/blob/master/images/ordinals1.png)

Perform arithmetic to build more complicated ordinals. All ordinals are represented in Cantor normal form:

![alt tag](https://github.com/ajcr/py-omega/blob/master/images/ordinals2.png)

You can easily build up the intimidating ordinal shown on [Wikipedia's page for ordinal arithmetic](https://en.wikipedia.org/wiki/Ordinal_arithmetic#Cantor_normal_form)... and then use it in calculations:

![alt tag](https://github.com/ajcr/py-omega/blob/master/images/ordinals4.png)


Comparison operators also work exactly as they're meant to, so any two ordinals can be compared, and any inequality verified.


## Future

To be implemented one day soon...

- Veblen hierarchy, large countable ordinals.
- Visualisation of small countable ordinals (maybe).

