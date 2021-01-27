import logging
from typing import List

from simulation.SimulatedSystem import SimulatedSystem
from simulation.WorldState import WorldState
from model.equation.Equation import Equation


class Model(SimulatedSystem):

    def __init__(self, equations: List[Equation], fps: int = 5):
        super().__init__(fps)
        self.equations = equations

    def step(self, time_delta):
        logging.info("Starting a model step")
        # Get the latest state
        world_state = self.get_latest_world()

        updated_world = self.progress(time_delta, world_state)

        # Add the new world state to the world state list
        self.append_world(updated_world)

    def progress(self, time_delta, world_state: WorldState):
        # Apply each equation, changing the world state
        updates = {}
        for equation in self.equations:
            logging.info("Applying equation: %s", equation)
            u = equation.apply(world_state, time_delta)
            updates.update(u)

        updated_world = world_state.apply_assignment(updates)
        logging.info("New world state computed: %s", updated_world)
        return updated_world
