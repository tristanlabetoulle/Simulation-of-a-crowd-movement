import numpy as np
import array
from math import exp


a = np.array((3,2))
b = np.array((1,2))

print a-2
print np.dot((a-b),(a-b))**0.5
print exp(sum(a-b))

print round(37*0.5)