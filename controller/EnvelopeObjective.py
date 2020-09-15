from decimal import Decimal

from WorldState import WorldState
from controller.ControlObjective import ControlObjective


class EnvelopeObjective(ControlObjective):
    def __init__(self, variable: str, lower: Decimal, upper: Decimal):
        super().__init__(variable)
        self.lower = lower
        self.upper = upper

    def is_satisfied(self, world_state : WorldState):
        value = world_state.variables[self.variable]
        return self.lower < value < self.upper

    def distance_until_satisfied(self, world_state : WorldState):
        value = world_state.variables[self.variable]

        if value < self.lower:
            return self.lower - value
        else:
            return self.upper - value