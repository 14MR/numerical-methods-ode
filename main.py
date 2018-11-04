import math

import matplotlib.pyplot as plt
import numpy as np

INITIAL_X = 1.4
INITIAL_Y = -21.76698207998232
ENDING_X = 7
DELTA = 0.001
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

    x = [i for i in np.arange(x0, x + DELTA, DELTA)]
    y = []

    for i, v in enumerate(x):
        value = my_function(v, const)
        y.insert(i, value)

    return x, y


def euler(x0, y0, x):
    x = [i for i in np.arange(x0, x + DELTA, DELTA)]
    y = [y0]

    for i, v in enumerate(x):
        if i == 0:
            continue
        value = y[i - 1] + DELTA * f(x[i - 1], y[i - 1])
        y.insert(i, value)

    return x, y


def runge_kutta(x0, y0, x):
    def calculate(x, y):
        k1 = DELTA * f(x, y)
        k2 = DELTA * f(x + DELTA / 2, y + k1 / 2)
        k3 = DELTA * f(x + DELTA / 2, y + k2 / 2)
        k4 = DELTA * f(x + DELTA, y + k3)

        return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6

    x = [i for i in np.arange(x0, x + DELTA, DELTA)]
    y = [y0]

    for i, v in enumerate(x):
        if i == 0:
            continue

        value = calculate(x[i - 1], y[i - 1])

        y.insert(i, value)

    x, y = x[:len(y)], y

    return x, y


x1, y1 = reference_solution(1, 0.5, INITIAL_X)
x2, y2 = reference_solution(INITIAL_X, INITIAL_Y, ENDING_X)
x = x1 + x2
y = y1 + y2
fig, ax = plt.subplots()
ax.plot(x[:len(y)], y[:len(x)])
ax.set_ylim(-20, 20)

x1, y1 = euler(1, 0.5, INITIAL_X)
x2, y2 = euler(INITIAL_X, INITIAL_Y, ENDING_X)

x = x1 + x2
y = y1 + y2
ax.plot(x[:len(y)], y[:len(x)])

x1, y1 = runge_kutta(1, 0.5, INITIAL_X)
x2, y2 = runge_kutta(INITIAL_X, INITIAL_Y, ENDING_X)

x = x1 + x2
y = y1 + y2

ax.plot(x[:len(y)], y[:len(x)])
fig.savefig("runge.png")
