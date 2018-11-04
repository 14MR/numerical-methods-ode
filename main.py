# import numpy as np
import math

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

INITIAL_X = 1
INITIAL_Y = 0.5
ENDING_X = 1.37
DELTA = 0.01
my_asymp_coordinate = 1.37
MIN_Y = -100
MAX_Y = 10000


def f(x, y):
    return y * y * math.exp(x) + 2 * y


def reference_solution(x0, y0, x):
    def const_function(x, y):
        # return -(3 * math.exp(2 * x) / y + math.exp(3 * x))
        return 6 * math.exp(2) + math.exp(3)

    def my_function(x, constant):
        return (3 * math.exp(2 * x)) / (constant - math.exp(3 * x))

    const = const_function(x0, y0)

    x = [i for i in np.arange(x0, x + DELTA, DELTA)]  # TODO: посмотреть границы для правой части
    y = []

    try:
        for i, v in enumerate(x):
            y.insert(i, my_function(v, const))
    except:
        pass

    return x, y


def euler(x0, y0, x):
    def function_y(x):
        if x <= INITIAL_X:
            return INITIAL_Y
        else:
            return function_y(x - DELTA) + DELTA * f(x - DELTA, function_y(x - DELTA))

    x = [i for i in np.arange(x0, x + DELTA, DELTA)]

    y = [y0]

    for i, v in enumerate(x):
        if i == 0:
            continue
        value = y[i - 1] + DELTA * f(x[i - 1], y[i - 1])
        if value > MAX_Y:
            value = float('inf')
        y.insert(i, value)

    x, y = x[:len(y)], y

    return x, y


def runge_kutta(x0, y0, x):
    def calculate(x, y):
        k1 = DELTA * f(x, y)
        k2 = DELTA * f(x + DELTA / 2, y + k1 / 2)
        k3 = DELTA * f(x + DELTA / 2, y + k2 / 2)
        k4 = DELTA * f(x + DELTA, y + k3)

        return y + (k1 + k2 + k3 + k4) / 6

    x = [i for i in np.arange(x0, x + DELTA, DELTA)]  # TODO: посмотреть границы для правой части
    y = [y0]

    # try:
    for i, v in enumerate(x):
        if i == 0:
            continue

        value = calculate(x[i - 1], y[i - 1])
        if value > MAX_Y:
            value = float('inf')

        y.insert(i, value)
    # except:
    #     pass

    x, y = x[:len(y)], y

    return x, y


x, y = reference_solution(INITIAL_X, INITIAL_Y, ENDING_X)

# for i, v in enumerate(x):
#     print(x[i], y[i], '\n')

fig, ax = plt.subplots()
ax.plot(x[:len(y)], y)
fig.savefig("reference.png")

x, y = euler(INITIAL_X, INITIAL_Y, ENDING_X)
fig, ax = plt.subplots()
# ax.axvline(linewidth=my_asymp_coordinate, color='r')
ax.plot(x, y)
fig.savefig("euler.png")

x, y = runge_kutta(INITIAL_X, INITIAL_Y, ENDING_X)
fig, ax = plt.subplots()
ax.plot(x, y)
fig.savefig("runge.png")
