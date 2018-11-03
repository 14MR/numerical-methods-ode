# import numpy as np
import math

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

INITIAL_X = 1
INITIAL_Y = 0.5
STARTING_X = 7


def reference_solution():
    def const_function(x, y):
        # return -(3 * math.exp(2 * x) / y + math.exp(3 * x))
        return 3 * math.exp(1) + math.exp(3 / 2)

    def my_function(x, constant):
        return -(3 * math.exp(2 * x)) / (constant + math.exp(3 * x))

    const = const_function(INITIAL_X, INITIAL_Y)

    x = [i for i in range(STARTING_X, 1000)]
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
