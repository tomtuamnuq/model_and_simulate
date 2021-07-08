"""Module to select which simulation to run."""
from functools import partial
import chaos.chaos_main as chaos_sim
import model_and_simulate.molecular_dynamics.molecule_main as molecular_sim
import road_traffic_microscopic.traffic_main as traffic_sim
import model_and_simulate.utilities.pygame_simple as pygame_simple


simulations = {
    "chaos_lorenz": partial(chaos_sim.chaos_main, "lorenz", "k"),
    "chaos_aizawa": partial(chaos_sim.chaos_main, "aizawa", "c"),
    "molecular": molecular_sim.molecule_main,
    "traffic": traffic_sim.traffic_main,
}
simulation_key = "traffic"  # change to select simulation to run

pygame_simulations = [molecular_sim.molecule_main, traffic_sim.traffic_main]


def pygame_main(simulation_main):
    """Runs the simulation within pygame logic."""
    reset = True
    while reset:
        reset = simulation_main()
    pygame_simple.quit_pygame()


if __name__ == "__main__":
    simulation = simulations[simulation_key]
    if simulation in pygame_simulations:
        pygame_main(simulation)
    else:
        simulation()
