from decimal import Decimal

from src.core.model.equation.equation import Equation
from src.core.simulation import world_state


class InitializingEquation(Equation):

    def initialize(self, world_state: world_state) -> (str, Decimal):
        raise ("Equation " + str(self.__class__) + " initialize not implemented!")
