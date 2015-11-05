# py-omega

Transfinite ordinal arithmetic in Python, printed in beautiful LaTeX.

The infinite made simple. Allows transfinite ordinals to be easily constructed and compared, and then added, multiplied or raised to transfinite powers.

## Overview

Works with Python 3.2 and higher. Use a Jupyter/IPython notebook/qtconsole to have the output properly rendered (this makes working with ordinals much, much easier).

Here's a quick demonstration...

Create initial ordinals with the `omega` function. Arbitrarily indexes are supported:

![alt tag](https://github.com/ajcr/py-omega/blob/master/images/ordinals1.png)

Perform arithmetic to build more complicated ordinals. All ordinals are represented in Cantor normal form:

![alt tag](https://github.com/ajcr/py-omega/blob/master/images/ordinals2.png)

You can easily build up the intimidating ordinal shown on [Wikipedia's page for ordinal arithmetic](https://en.wikipedia.org/wiki/Ordinal_arithmetic#Cantor_normal_form)... and then use it in calculations:

![alt tag](https://github.com/ajcr/py-omega/blob/master/images/ordinals4.png)


Comparison operators also work exactly as they're meant to, so any two ordinals can be compared and any inequality verified.


## Future

To be implemented very soon...

- Visualisation of small countable ordinals (maybe).
- More exotic species of ordinals (maybe).

To be tidied up soon...

- Refactor code and make into a proper module
- Eliminate/reduce need for explicit type-checking in methods

Bug reports and feature requests are welcomed, as are pull requests.

