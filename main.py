# import numpy as np
import math

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

INITIAL_X = 1
INITIAL_Y = 0.5
ENDING_X = 7
DELTA = 0.01
my_asymp_coordinate = 1.37
MIN_Y = -100
MAX_Y = 10000


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


def euler():
    def function_y(x):
        if x <= INITIAL_X:
            return INITIAL_Y
        else:
            return function_y(x - DELTA) + DELTA * f(x - DELTA, function_y(x - DELTA))

    x = [i for i in np.arange(INITIAL_X, ENDING_X + DELTA, DELTA)]

    y = [INITIAL_Y]
    deleted_x = []

    before_asympt = [i for i in x if i < my_asymp_coordinate - 2 * DELTA]
    after_asympt = [i for i in x if 4 < i < ENDING_X]

    #
    # for i in before_asympt:
    #     print(i, "\n")

    for i, v in enumerate(x):
        if i == 0:
            continue
        value = y[i - 1] + DELTA * f(x[i - 1], y[i - 1])
        if value > MAX_Y:
            value = float('inf')
        y.insert(i, value)

    # print("\nasymp\n")

    # for i, v in enumerate(after_asympt):
    #
    #     if i == 0:
    #         y.insert(len(y), MIN_Y)
    #         continue
    #
    #     cur_index = len(y)
    #
    #     value = y[cur_index - 1] + DELTA * f(after_asympt[i - 1], y[cur_index - 1])
    #     # print(i, v, value, ' \n')
    #
    #     y.insert(cur_index, value)

    x, y = x[:len(y)], y

    return x, y


x, y = reference_solution()

# for i, v in enumerate(x):
#     print(x[i], y[i], '\n')

fig, ax = plt.subplots()
ax.plot(x[:len(y)], y)
fig.savefig("reference.png")

x, y = euler()
fig, ax = plt.subplots()
# ax.axvline(linewidth=my_asymp_coordinate, color='r')
ax.plot(x, y)
fig.savefig("euler.png")
