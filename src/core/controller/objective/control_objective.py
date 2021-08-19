from src.core.simulation.world_state import WorldState


class ControlObjective:
    def __init__(self, variable: str):
        self.variable = variable

    def is_satisfied(self, world_state: WorldState):
        raise Exception("Control Objective " + str(self.__class__) + " does not implement is_satisfied. ")

    def distance_until_satisfied(self, world_state: WorldState):
        raise Exception("Control Objective " + str(self.__class__) + " does not implement distance_until_satisfied. ")
