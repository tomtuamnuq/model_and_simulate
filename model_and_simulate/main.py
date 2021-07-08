"""Module to select which simulation to run."""
from functools import partial
import chaos.chaos_main as chaos_sim
import model_and_simulate.molecular_dynamics.molecule_main as molecular_sim
import road_traffic_microscopic.traffic_main as traffic_sim
import model_and_simulate.utilities.pygame_simple as pygame_simple


pygame_simulations = {
    "Molecule_Simulation": molecular_sim.MoleculeVisualization,
    "Microscopic_Traffic": traffic_sim.traffic_main,
}

matplotlib_simulations = {
    "chaos_lorenz": partial(chaos_sim.chaos_main, "lorenz", "k"),
    "chaos_aizawa": partial(chaos_sim.chaos_main, "aizawa", "c"),
}

simulation_key = "Molecule_Simulation"  # change to select simulation to run


def pygame_main():
    """Runs the simulation within pygame logic."""
    reset = True
    while reset:
        simulation = pygame_simulations[simulation_key](simulation_key)
        reset = simulation.main()
    pygame_simple.quit_pygame()


if __name__ == "__main__":
    if simulation_key in pygame_simulations:
        pygame_main()
    else:
        simulation_main = matplotlib_simulations[simulation_key]
        simulation_main()
