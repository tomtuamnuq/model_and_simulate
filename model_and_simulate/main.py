"""Module to select which simulation to run."""
import model_and_simulate.utilities.pygame_simple as pygame_simple

from base_start_menu import pygame_simulations, matplotlib_simulations, BaseStartScreen


def run_pygame_main() -> bool:
    """Runs the simulation within pygame logic."""
    reset = True
    while reset:
        simulation = pygame_simulations[simulation_key](simulation_key)
        reset, back_to_start = simulation.main()
        if back_to_start:
            return True
    return False


if __name__ == "__main__":

    running = True
    while running:
        base_start_screen = BaseStartScreen()
        simulation_key, running = base_start_screen.show_start_screen()
        if running:
            if simulation_key in pygame_simulations:
                running = run_pygame_main()
            else:
                simulation_main = matplotlib_simulations[simulation_key]
                simulation_main()
    pygame_simple.quit_pygame()
