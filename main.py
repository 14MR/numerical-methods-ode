import matplotlib.pyplot as plt

from solver import ODESolver

solver = ODESolver()
reference_x, reference_y = solver.calculate_reference()
fig, ax = plt.subplots()
ax.scatter(reference_x, reference_y)
ax.set_ylim(-30, 40)

x, y = solver.calculate_euler()
ax.scatter(x, y)

err_fig, err_ax = plt.subplots()
err, max = solver.calculate_euler_errors()

err_ax.plot(err)
err_fig.savefig("err_euler.png")

x, y = solver.calculate_improved_euler()
ax.scatter(x, y)

err_fig, err_ax = plt.subplots()
err, max = solver.calculate_improved_euler_errors()
err_ax.plot(err)
err_fig.savefig("err_improved_euler.png")

x, y = solver.calculate_runge_kutta()

ax.scatter(x, y)

err_fig, err_ax = plt.subplots()
err, max = solver.calculate_runge_kutta_errors()

err_ax.plot(err)
err_fig.savefig("err_runge.png")

fig.savefig("runge.png")
