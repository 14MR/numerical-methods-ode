import os

import click
import matplotlib.pyplot as plt

from solver import ODESolver

directory_for_files = './data/'


@click.group()
def cli():
    if not os.path.exists(directory_for_files):
        click.echo(f'Directory {directory_for_files} do not exist, it will be created.')
        os.makedirs(directory_for_files)


@cli.command()
@click.option('-x0', default=1.0, help='X coordinate for IVP')
@click.option('-y0', default=0.5, help='Y coordinate for IVP')
@click.option('-x', default=7.0, help='Ending X coordinate')
@click.option('-n', default=10000, help='Number of grid steps')
def plot_graphs(x0, y0, n, x):
    """Command for plotting graphs"""

    solver = ODESolver(initial_x=x0, initial_y=y0, n=n, ending_x=x)
    reference_x, reference_y = solver.calculate_reference()
    fig, ax = plt.subplots()
    plt.xlabel('x coordinate')
    plt.ylabel('y coordinate')
    ax.plot(reference_x, reference_y)
    ax.set_ylim(-23, 16)

    x, y = solver.calculate_euler()
    ax.plot(x, y)

    err_fig, err_ax = plt.subplots()
    err, max = solver.calculate_euler_errors()
    plt.xlabel('x coordinate')
    plt.ylabel('size of error')
    err_ax.plot(err)
    err_fig.savefig(f"{directory_for_files}local_err_euler.png", bbox_inches="tight")

    x, y = solver.calculate_improved_euler()
    ax.plot(x, y)

    err_fig, err_ax = plt.subplots()
    err, max = solver.calculate_improved_euler_errors()
    err_ax.plot(err)
    plt.xlabel('x coordinate')
    plt.ylabel('size of error')
    err_fig.savefig(f"{directory_for_files}local_err_improved_euler.png", bbox_inches="tight")

    x, y = solver.calculate_runge_kutta()

    ax.plot(x, y)

    err_fig, err_ax = plt.subplots()
    err, max = solver.calculate_runge_kutta_errors()
    plt.xlabel('x coordinate')
    plt.ylabel('size of error')
    err_ax.plot(err)
    err_fig.savefig(f"{directory_for_files}local_err_runge.png", bbox_inches="tight")

    fig.savefig(f"{directory_for_files}all.png", bbox_inches="tight")

    click.echo(f'Generating succeed. Check out your {directory_for_files} directory.')


@cli.command()
@click.option('--start', default=100, help='Starting number of grid steps')
@click.option('--end', default=10000, help='Ending number of grid steps')
@click.option('--step', default=100, help='Size of each step')
def global_errors(start, end, step):
    """Calculates global error in given range"""

    click.echo(f'Calculating global errors for segment [{start};{end}] with step {step}.')

    euler_errors = []
    improved_euler_errors = []
    runge_kutta_errors = []

    r = range(int(start), int(end), int(step))

    with click.progressbar(r) as bar:
        for i in bar:
            solver = ODESolver(initial_y=0.5, initial_x=1, ending_x=7, n=i)
            solver.calculate_reference()

            solver.calculate_euler()
            err, max = solver.calculate_euler_errors()
            euler_errors.append(max)

            solver.calculate_improved_euler()
            err, max = solver.calculate_improved_euler_errors()
            improved_euler_errors.append(max)

            solver.calculate_runge_kutta()
            err, max = solver.calculate_runge_kutta_errors()
            runge_kutta_errors.append(max)

    err_fig, err_ax = plt.subplots()
    plt.xlabel('number of grid steps')
    plt.ylabel('max local error')
    err_ax.plot(euler_errors)
    err_fig.savefig(f"{directory_for_files}global_euler.png", bbox_inches="tight")

    err_fig, err_ax = plt.subplots()
    plt.xlabel('number of grid steps')
    plt.ylabel('max local error')
    err_ax.plot(improved_euler_errors)
    err_fig.savefig(f"{directory_for_files}global_improved_euler.png", bbox_inches="tight")

    err_fig, err_ax = plt.subplots()
    plt.xlabel('number of grid steps')
    plt.ylabel('max local error')
    err_ax.plot(runge_kutta_errors)
    err_fig.savefig(f"{directory_for_files}global_runge_kutta.png", bbox_inches="tight")


if __name__ == '__main__':
    cli()
