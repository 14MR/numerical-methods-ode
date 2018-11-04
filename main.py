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
@click.option('-x', default=1, help='X coordinate for IVP')
@click.option('-y', default=0.5, help='Y coordinate for IVP')
@click.option('-n', default=10000, help='Number of grid steps')
def plot_graphs(x, y, n):
    """Command for plotting graphs"""
    solver = ODESolver(initial_x_1=x, initial_y_1=y, n=n)
    reference_x, reference_y = solver.calculate_reference()
    fig, ax = plt.subplots()
    ax.plot(reference_x, reference_y)
    ax.set_ylim(-23, 16)

    x, y = solver.calculate_euler()
    ax.plot(x, y)

    err_fig, err_ax = plt.subplots()
    err, max = solver.calculate_euler_errors()

    err_ax.plot(err)
    err_fig.savefig(f"{directory_for_files}err_euler.png")

    x, y = solver.calculate_improved_euler()
    ax.plot(x, y)

    err_fig, err_ax = plt.subplots()
    err, max = solver.calculate_improved_euler_errors()
    err_ax.plot(err)
    err_fig.savefig(f"{directory_for_files}err_improved_euler.png")

    x, y = solver.calculate_runge_kutta()

    ax.plot(x, y)

    err_fig, err_ax = plt.subplots()
    err, max = solver.calculate_runge_kutta_errors()

    err_ax.plot(err)
    err_fig.savefig(f"{directory_for_files}err_runge.png")

    fig.savefig(f"{directory_for_files}all.png")


@cli.command()
@click.option('--start', default=1, help='Starting number of grid steps')
@click.option('--end', default=0.5, help='Ending number of grid steps')
def global_errors(start, end):
    """Calculates global error in given range"""

    euler_errors, improved_euler_errors, runge_kutta_errors = ODESolver.investigate_global_errors(int(start), int(end))

    err_fig, err_ax = plt.subplots()
    err_ax.plot(euler_errors)
    err_fig.savefig(f"{directory_for_files}global_euler.png")

    err_fig, err_ax = plt.subplots()
    err_ax.plot(improved_euler_errors)
    err_fig.savefig(f"{directory_for_files}improved_euler.png")

    err_fig, err_ax = plt.subplots()
    err_ax.plot(runge_kutta_errors)
    err_fig.savefig(f"{directory_for_files}runge_kutta.png")


if __name__ == '__main__':
    cli()
