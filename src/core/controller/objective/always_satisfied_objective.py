from src.core.simulation.world_state import WorldState
from src.core.controller.objective.control_objective import ControlObjective


class AlwaysSatisfiedObjective(ControlObjective):
    def __init__(self, variable: str):
        super().__init__(variable)

    def is_satisfied(self, world_state: WorldState):
        return True

    def distance_until_satisfied(self, world_state: WorldState):
        return 0


