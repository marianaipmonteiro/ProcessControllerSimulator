from typing import List

from WorldState import WorldState
from model.Equation import Equation
from model.Model import Model


class StaticInitializedModel(Model):

    def __init__(self, equations: List[Equation], initial_world_state: WorldState):
        super().__init__(equations)
        self.initial_world_state = initial_world_state

    def initialization(self, world_states):
        #todo call equation initialization
        initial_values = {}
        for equation in self.equations:
            initial_value = equation.initialize(self.initial_world_state.apply_assignment(initial_values))
            initial_values.update(initial_value)
        initial_world = self.initial_world_state.apply_assignment(initial_values)
        #print("Initialization!:\n" + str(initial_world))
        #print("========================================================")
        world_states.append(initial_world)


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
        #print("New state: " + str(world_state), flush=True)
