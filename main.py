# import numpy as np
import math

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

INITIAL_X = 1
INITIAL_Y = 0.5
ENDING_X = 7
DELTA = 0.1


def f(x, y):
    return y * y * math.exp(x) + 2 * y


def reference_solution():
    def const_function(x, y):
        # return -(3 * math.exp(2 * x) / y + math.exp(3 * x))
        return 6 * math.exp(2) + math.exp(3)

    def my_function(x, constant):
        return (3 * math.exp(2 * x)) / (constant - math.exp(3 * x))

    const = const_function(INITIAL_X, INITIAL_Y)

    x = [i for i in np.arange(INITIAL_X, ENDING_X + DELTA, DELTA)]  # TODO: посмотреть границы для правой части
    y = []

    try:
        for i, v in enumerate(x):
            y.insert(i, my_function(v, const))
    except:
        pass

    return x, y


x, y = reference_solution()

fig, ax = plt.subplots()
ax.plot(x[:len(y)], y)

fig.savefig("test.png")
# plt.show()
