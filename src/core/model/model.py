import logging
from typing import List

from .equation.equation import Equation
from src.core.simulation.simulated_system import SimulatedSystem
from src.core.simulation.world_state import WorldState


class Model(SimulatedSystem):

    def __init__(self, equations: List[Equation], fps: int = 5):
        super().__init__(fps)
        self.equations = equations

    def step(self, time_delta):
        logging.debug("Starting a model step")
        # Get the latest state
        world_state = self.get_latest_world()

        updated_world = self.progress(time_delta, world_state)

        # Add the new world state to the world state list
        self.append_world(updated_world)

    def progress(self, time_delta, world_state: WorldState):
        # Apply each equation, changing the world state
        updates = {}
        for equation in self.equations:
            # logging.info("Applying equation: %s", equation)
            u = equation.apply(world_state, time_delta)
            updates.update(u)

        updated_world = world_state.apply_assignment(updates)
        # logging.info("New world state computed: %s", updated_world)
        return updated_world
