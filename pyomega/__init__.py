from .ordinals import Ordinal

# useful to allow expose this  constructor method
# as a function, allowing limit ordinals to be
# construncted vert easily 
omega = Ordinal.from_index

# first countably infinite ordinal
w = omega(0)
# first uncountable ordinal
w1 = omega(1)
