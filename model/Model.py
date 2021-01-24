import threading
from typing import List

from simulation.SimulatedSystem import SimulatedSystem
from simulation.Simulation import RunningFlag
from simulation.WorldState import WorldState
from model.equation.Equation import Equation


class Model(SimulatedSystem):

    def __init__(self, equations: List[Equation], fps: int = 5):
        super().__init__(fps)
        self.equations = equations

    def step(self, time_delta, world_states: List[WorldState]):
        # Get the latest state
        world_state = world_states[-1]
        # Apply each equation, changing the world state
        updates = {}
        for equation in self.equations:
            u = equation.apply(world_state, time_delta)
            updates.update(u)

        # Add the new world state to the world state list
        world_states.append(world_state.apply_assignment(updates))
