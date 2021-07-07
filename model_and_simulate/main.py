"""Module to select which simulation to run."""
from functools import partial
import chaos.chaos_main as chaos_sim
import model_and_simulate.molecular_dynamics.molecule_main as molecular_sim
import model_and_simulate.utilities.pygame_simple as pygame_simple


simulations = {
    "chaos_lorenz": partial(chaos_sim.chaos_main, "lorenz", "k"),
    "chaos_aizawa": partial(chaos_sim.chaos_main, "aizawa", "c"),
    "molecular": molecular_sim.molecule_main,
}
simulation_key = "molecular"  # change to select simulation to run

pygame_simulations = [molecular_sim.molecule_main]

if __name__ == "__main__":
    simulation = simulations[simulation_key]
    if simulation in pygame_simulations:
        reset = True
        while reset:
            reset = simulation()
        pygame_simple.quit_pygame()
    else:
        simulation()
