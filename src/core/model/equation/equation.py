from src.core.simulation.world_state import WorldState, Decimal


class Equation:
    def apply(self, world_state: WorldState, time_delta: Decimal) -> (str, Decimal):
        raise ("Equation " + str(self.__class__) + " apply not implemented!")

    def __str__(self):
        return self.__class__.__name__
