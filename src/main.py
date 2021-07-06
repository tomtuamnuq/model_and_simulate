"""Module to select which simulation to run."""
import src.molecular_dynamics.molecule_main as molecular_sim
import src.utilities.pygame_simple as pygame_simple

simulation = molecular_sim.molecule_main  # change to select simulation

if __name__ == "__main__":
    reset = True
    while reset:
        reset = simulation()
    pygame_simple.quit_pygame()
