import logging
from decimal import Decimal
from typing import List, Dict

from .equation.initializing_equation import InitializingEquation
from src.core.simulation.world_initializer import WorldInitializer
from src.core.simulation.world_state import WorldState
from.model import Model


class SelfInitializingModel(Model, WorldInitializer):

    def __init__(self, equations: List[InitializingEquation], constants: Dict[str, Decimal], mvs: List[str], cvs: List[str], fps: int = 5):
        """
        Creates a model that also initializes the world.
        :param equations: A list of InitializingEquations in the order in which they should be initialized. Each equation has access to the variables initialized by the previous equation
        :param constants: The constants of the system
        :param mvs: The manipulated variables, which are the variables which can be controlled by the controller
        :param cvs: The controlled variables, which counterintuitively are exactly those which cannot be controlled by the controller.
        """
        super().__init__(equations, fps)#TODO fix super ambiguity
        self.initializing_equations = equations
        self.constants = constants
        self.mvs = mvs
        self.cvs = cvs

    def create_initial_world(self) -> WorldState:
        logging.info("Creating initial world based on InitializingEquations!")
        # Create a world state with no variables
        world_state = WorldState(constants=self.constants, variables={}, mvs=self.mvs, cvs=self.cvs)

        # Each equation adds some variables in
        for equation in self.initializing_equations:
            logging.info("Calling initializing equation %s.", equation)
            initialized_variables = equation.initialize(world_state)
            world_state = world_state.apply_assignment(initialized_variables)

        logging.info("Initial world state computed: %s.", world_state)

        return world_state

