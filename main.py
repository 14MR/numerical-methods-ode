import math

import matplotlib.pyplot as plt
import numpy as np

INITIAL_X_1 = 1
INITIAL_Y_1 = 0.5
ENDING_X_1 = 1.3889999999999572

INITIAL_X_2 = 1.4
INITIAL_Y_2 = -21.76698207998232
ENDING_X_2 = 7
DELTA = 0.001


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


def improved_euler(x0, y0, x):
    x = [i for i in np.arange(x0, x + DELTA, DELTA)]
    y = [y0]

    for i, v in enumerate(x):
        if i == 0:
            continue
        value = y[i - 1] + DELTA / 2 * (f(x[i - 1], y[i - 1]) + f(x[i], y[i - 1] + DELTA * f(x[i - 1], y[i - 1])))
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


def extract_errors(reference, calculated):
    erros = []
    max = 0

    for i in range(len(reference) - 1):
        if (i > 0 and abs(
                reference[i] - reference[i - 1]) < DELTA) or i == 0:  # if our step is bigger than delta => we had an
            # asymptote
            value = abs(reference[i] - calculated[i])
            if value != float('inf'):  # let's skip errors which is inf
                erros.append(value)
                if max < value:
                    max = value

    return erros, max


x1, y1 = reference_solution(INITIAL_X_1, INITIAL_Y_1, ENDING_X_1)
x2, y2 = reference_solution(INITIAL_X_2, INITIAL_Y_2, ENDING_X_2)
reference_x = x1 + x2
reference_y = y1 + y2

fig, ax = plt.subplots()
ax.scatter(reference_x, reference_y)
ax.set_ylim(-30, 40)

x1, y1 = euler(1, 0.5, INITIAL_X_2)
x2, y2 = euler(INITIAL_X_2, INITIAL_Y_2, ENDING_X_2)

x = x1 + x2
y = y1 + y2
ax.scatter(x, y)

err_fig, err_ax = plt.subplots()
erros, max = extract_errors(reference_y, y)
err_ax.plot(erros)
err_fig.savefig("err_euler.png")

x1, y1 = improved_euler(1, 0.5, INITIAL_X_2)
x2, y2 = improved_euler(INITIAL_X_2, INITIAL_Y_2, ENDING_X_2)

x = x1 + x2
y = y1 + y2
ax.scatter(x, y)

err_fig, err_ax = plt.subplots()
erros, max = extract_errors(reference_y, y)
err_ax.plot(erros)
err_fig.savefig("err_improved_euler.png")

x1, y1 = runge_kutta(1, 0.5, INITIAL_X_2)
x2, y2 = runge_kutta(INITIAL_X_2, INITIAL_Y_2, ENDING_X_2)

x = x1 + x2
y = y1 + y2

ax.scatter(x, y)

err_fig, err_ax = plt.subplots()
erros, max = extract_errors(reference_y, y)
err_ax.plot(erros)
err_fig.savefig("err_runge.png")

fig.savefig("runge.png")
