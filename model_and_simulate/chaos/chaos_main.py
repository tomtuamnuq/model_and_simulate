"""Module with function to set parameters and run the chaos simulation."""
import numpy as np
from .chaos_simulation import ChaosSimulation
import matplotlib.pyplot as plt

from .lorenz import lorenz_differential_equation


def chaos_main() -> None:
    """Performs the simulation of the system of differential equations."""
    ode_system = lorenz_differential_equation
    simulation = ChaosSimulation(ode_system, dimensions=3)
    interim_point, interim_time = simulation.run_into_chaos()
    if interim_point is None:
        print("Solver was not successful to get the ode into chaotic state.")
    else:
        data = simulation.get_chaotic_data(chaotic_point=interim_point, time_start=interim_time)
        if data is None:
            print("Solver was not successful to produce chaotic data.")
        else:
            if data.shape[0] == 3:
                plot3D_bifurcation_diagram(data)


def plot3D_bifurcation_diagram(data: np.ndarray):
    """Plots the data as bifurcation diagram with grey opacity by using `plot3D`."""
    plt.figure(figsize=(9, 9))
    ax = plt.axes(projection="3d")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.plot3D(data[0], data[1], data[2], ",k", alpha=0.5)
    plt.show()
