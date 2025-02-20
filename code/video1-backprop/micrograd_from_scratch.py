import math
import numpy as np
import matplotlib.pyplot as plt

# scalar valued function f of x
# scalar = there's a size but no direction.

def f(x):
    return 3*x**2 - 4*x + 5 # 3x^2 - 4x + 5
# print(f(3.0)) # prints 20.0

xs = np.arange(-5, 5, 0.25) # return an array from -5 (inclusive) to 5 (exclusive) in steps of 0.25
ys = f(xs) # call our function f on the array
plt.plot(xs, ys)
