from WorldState import WorldState, Decimal


class Equation:
    #def __init__(self, name: str):

    def initialize(self, world_state: WorldState) -> (str, Decimal):
        raise ("Equation " + str(self.__class__) + " initialize not implemented!")

    def apply(self, world_state: WorldState, time_delta: Decimal) -> (str, Decimal):
        raise("Equation "+ str(self.__class__) + " apply not implemented!")


