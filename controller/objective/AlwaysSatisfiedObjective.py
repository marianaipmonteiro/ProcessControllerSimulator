from decimal import Decimal

from simulation.WorldState import WorldState
from controller.objective.ControlObjective import ControlObjective


class AlwaysSatisfiedObjective(ControlObjective):
    def __init__(self, variable: str):
        super().__init__(variable)

    def is_satisfied(self, world_state: WorldState):
        return True

    def distance_until_satisfied(self, world_state: WorldState):
        return 0


