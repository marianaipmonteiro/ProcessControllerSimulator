from decimal import Decimal

from model.equation.Equation import Equation
from simulation import WorldState


class InitializingEquation(Equation):

    def initialize(self, world_state: WorldState) -> (str, Decimal):
        raise ("Equation " + str(self.__class__) + " initialize not implemented!")
