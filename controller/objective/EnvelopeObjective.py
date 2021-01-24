from decimal import Decimal

from simulation.WorldState import WorldState
from controller.objective.ControlObjective import ControlObjective


class EnvelopeObjective(ControlObjective):
    def __init__(self, variable: str, lower: Decimal, upper: Decimal):
        super().__init__(variable)
        self.lower = lower
        self.upper = upper

    def is_satisfied(self, world_state: WorldState):
        value = world_state.variables[self.variable]
        return self.lower < value < self.upper

    def distance_until_satisfied(self, world_state: WorldState):
        if self.is_satisfied(world_state):
            return 0

        value = world_state.variables[self.variable]

        if value < self.lower:
            return self.lower - value
        else:
            return self.upper - value

