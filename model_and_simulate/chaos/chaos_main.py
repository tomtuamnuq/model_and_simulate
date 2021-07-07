"""Module with function to set parameters and run the chaos simulation."""
import numpy as np
from .chaos_simulation import ChaosSimulation
import matplotlib.pyplot as plt

from .lorenz import lorenz_differential_equation
from .aizawa import aizawa_differential_equation

ode_systems = {"lorenz": lorenz_differential_equation, "aizawa": aizawa_differential_equation}
ode_dimensions = {"lorenz": 3, "aizawa": 3}
start_points = {"lorenz": np.asarray([1, 1, 1]), "aizawa": np.asarray([0.1, 0, 0])}
num_iterations = {"lorenz": 100, "aizawa": 5000}


def chaos_main(ode_system_key: str, color: str) -> None:
    """Performs the simulation of the system of differential equations."""
    ode_system = ode_systems[ode_system_key]
    dimensions = ode_dimensions[ode_system_key]
    start_point = start_points.get(ode_system_key)
    num_iter = num_iterations[ode_system_key]
    simulation = ChaosSimulation(ode_system, dimensions=dimensions, start_point=start_point)
    interim_point, interim_time = simulation.run_into_chaos()
    if interim_point is None:
        print("Solver was not successful to get the ode into chaotic state.")
    else:
        print("Got system into chaotic state.")
        data = simulation.get_chaotic_data(
            chaotic_point=interim_point, time_start=interim_time, num_steps=num_iter
        )
        if data is None:
            print("Solver was not successful to produce chaotic data.")
        else:
            print("Got chaotic data.")
            if dimensions == 3:
                plot3D_bifurcation_diagram(data, color=color)


def plot3D_bifurcation_diagram(
    data: np.ndarray, marker: str = ",", color: str = "c", alpha: float = 0.5
):
    """Plots the data as bifurcation diagram with `color` opacity by using `plot3D`."""
    plt.figure(figsize=(9, 9))
    ax = plt.axes(projection="3d")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.plot3D(data[0], data[1], data[2], marker + color, alpha=alpha)
    plt.show()
