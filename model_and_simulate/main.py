"""Module to select which simulation to run."""
import chaos.chaos_main as chaos_sim
import model_and_simulate.molecular_dynamics.molecule_main as molecular_sim
import model_and_simulate.utilities.pygame_simple as pygame_simple

simulations = [chaos_sim.chaos_main, molecular_sim.molecule_main]
simulation = chaos_sim.chaos_main  # change to select simulation to run

pygame_simulations = [molecular_sim.molecule_main]

if __name__ == "__main__":
    if simulation in pygame_simulations:
        reset = True
        while reset:
            reset = simulation()
        pygame_simple.quit_pygame()
    else:
        simulation()
