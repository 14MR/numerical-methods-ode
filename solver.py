import math

import numpy as np


class ODESolver:
    ASYMPTOTE = 1.37  # some day it will be not hardcoded but not today
    INITIAL_X_1 = 1
    INITIAL_Y_1 = 0.5
    ENDING_X_1 = 1.3889

    INITIAL_X_2 = 1.4
    INITIAL_Y_2 = -21.76698207998232
    ENDING_X_2 = 7
    DELTA = 0.001

    reference_calculated = None
    euler_calculated = None
    improved_euler_calculated = None
    runge_kutta_calculated = None

    def __init__(self, initial_x, initial_y, ending_x, n=1000):
        if initial_x > self.ASYMPTOTE:
            self.INITIAL_X_1 = 0
            self.INITIAL_Y_1 = 0
            self.ENDING_X_1 = 0

            self.INITIAL_X_2 = initial_x
            self.INITIAL_Y_2 = initial_y
            self.ENDING_X_2 = ending_x
            self.DELTA = abs((ending_x - initial_x)) / n
        else:

            self.INITIAL_X_1 = initial_x
            self.INITIAL_Y_1 = initial_y
            self.ENDING_X_1 = self.ASYMPTOTE

            self.INITIAL_X_2 = 1.4  # precalculated and hardcoded IVP after asymptote
            self.INITIAL_Y_2 = -21.76698207998232
            self.ENDING_X_2 = ending_x
            self.DELTA = (abs((self.ASYMPTOTE - initial_x)) + abs((self.ENDING_X_2 - self.INITIAL_X_2))) / n

    def calculate_reference(self):
        x1, y1 = [], []
        if self.ENDING_X_1 != self.INITIAL_X_1:
            x1, y1 = self.reference_solution(self.INITIAL_X_1, self.INITIAL_Y_1, self.ENDING_X_1)
        x2, y2 = self.reference_solution(self.INITIAL_X_2, self.INITIAL_Y_2, self.ENDING_X_2)
        reference_x = x1 + x2
        reference_y = y1 + y2

        self.reference_calculated = reference_y

        return reference_x, reference_y

    def calculate_euler(self):
        x1, y1 = [], []
        if self.ENDING_X_1 != self.INITIAL_X_1:
            x1, y1 = self.euler(self.INITIAL_X_1, self.INITIAL_Y_1, self.ENDING_X_1)
        x2, y2 = self.euler(self.INITIAL_X_2, self.INITIAL_Y_2, self.ENDING_X_2)

        x = x1 + x2
        y = y1 + y2

        self.euler_calculated = y

        return x, y

    def calculate_euler_errors(self):
        errors, max = self.extract_errors(self.reference_calculated, self.euler_calculated)
        return errors, max

    def calculate_improved_euler(self):
        x1, y1 = [], []
        if self.ENDING_X_1 != self.INITIAL_X_1:
            x1, y1 = self.improved_euler(self.INITIAL_X_1, self.INITIAL_Y_1, self.ENDING_X_1)
        x2, y2 = self.improved_euler(self.INITIAL_X_2, self.INITIAL_Y_2, self.ENDING_X_2)

        x = x1 + x2
        y = y1 + y2

        self.improved_euler_calculated = y

        return x, y

    def calculate_improved_euler_errors(self):
        errors, max = self.extract_errors(self.reference_calculated, self.improved_euler_calculated)
        return errors, max

    def calculate_runge_kutta(self):
        x1, y1 = [], []
        if self.ENDING_X_1 != self.INITIAL_X_1:
            x1, y1 = self.runge_kutta(self.INITIAL_X_1, self.INITIAL_Y_1, self.ENDING_X_1)
        x2, y2 = self.runge_kutta(self.INITIAL_X_2, self.INITIAL_Y_2, self.ENDING_X_2)

        x = x1 + x2
        y = y1 + y2

        self.runge_kutta_calculated = y

        return x, y

    def calculate_runge_kutta_errors(self):
        errors, max = self.extract_errors(self.reference_calculated, self.runge_kutta_calculated)
        return errors, max

    @staticmethod
    def f(x, y):
        return y * y * math.exp(x) + 2 * y

    def reference_solution(self, x0, y0, x):
        def const_function(x, y):
            return 3 * math.exp(2 * x) / y + math.exp(3 * x)

        def my_function(x, constant):
            return (3 * math.exp(2 * x)) / (constant - math.exp(3 * x))

        const = const_function(x0, y0)

        x = [i for i in np.arange(x0, x + self.DELTA, self.DELTA)]
        y = []

        for i, v in enumerate(x):
            value = my_function(v, const)
            y.insert(i, value)

        return x, y

    def euler(self, x0, y0, x):
        x = [i for i in np.arange(x0, x + self.DELTA, self.DELTA)]
        y = [y0]

        for i, v in enumerate(x):
            if i == 0:
                continue
            value = y[i - 1] + self.DELTA * self.f(x[i - 1], y[i - 1])
            y.insert(i, value)

        x, y = x[:len(y)], y[:len(x)]

        return x, y

    def improved_euler(self, x0, y0, x):
        x = [i for i in np.arange(x0, x + self.DELTA, self.DELTA)]
        y = [y0]

        for i, v in enumerate(x):
            if i == 0:
                continue
            value = y[i - 1] + self.DELTA / 2 * (
                    self.f(x[i - 1], y[i - 1]) + self.f(x[i], y[i - 1] + self.DELTA * self.f(x[i - 1], y[i - 1])))
            y.insert(i, value)

        x, y = x[:len(y)], y[:len(x)]

        return x, y

    def runge_kutta(self, x0, y0, x):
        def calculate(x, y):
            k1 = self.DELTA * self.f(x, y)
            k2 = self.DELTA * self.f(x + self.DELTA / 2, y + k1 / 2)
            k3 = self.DELTA * self.f(x + self.DELTA / 2, y + k2 / 2)
            k4 = self.DELTA * self.f(x + self.DELTA, y + k3)

            return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6

        x = [i for i in np.arange(x0, x + self.DELTA, self.DELTA)]
        y = [y0]

        for i, v in enumerate(x):
            if i == 0:
                continue

            value = calculate(x[i - 1], y[i - 1])

            y.insert(i, value)

        x, y = x[:len(y)], y[:len(x)]

        return x, y

    def extract_errors(self, reference, calculated):
        errors = []
        max = 0

        for i in range(len(reference) - 1):
            if (i > 0 and abs(
                    reference[i] - reference[
                        i - 1]) < self.DELTA) or i == 0:  # if our step is bigger than delta => we had an
                # asymptote
                value = abs(reference[i] - calculated[i])
                if value != float('inf'):  # let's skip errors which is inf
                    errors.append(value)
                    if max < value:
                        max = value

        return errors, max
