from typing import Dict

from src.core.controller.constraint.constraint import Constraint
from src.core.controller.objective.control_objective import ControlObjective
from src.core.controller.problem.control_problem import ControlProblem


class MPCProblem(ControlProblem):
    """
    Specifies all the parameters of an MPC problem
    """

    def __init__(self, control_objectives: Dict[str, ControlObjective], constraints: Dict[str, Constraint],
                 weights: Dict[str, float], active_flags: Dict[str, bool], prediction_horizon: float,
                 optimisation_horizon: float, real_time: bool=True):
        """
        Creates a new MPCProblem
        :param control_objectives: a dictionary, where key is a cv and value is a control objective for that cv
        :param constraints: a dictionary, where key is a variable and vaue is a constraint on that variable
        :param weights: a dictionary, where key is a cv and value is the optimization weight of that cv
        :param active_flags: a dictionary, where key is a cv and value is a boolean specifying whether that cv should be considered in optimization
        :param prediction_horizon: The horizon up to which the controller predicts the evolution of the system
        :param optimisation_horizon:
        :param real_time: Whether the controller should act in real-time, or stop the world during optimization
        """
        super().__init__(control_objectives, constraints, real_time)
        self.weights = weights
        self.prediction_horizon = prediction_horizon
        self.active_flags = active_flags
        self.optimisation_horizon = optimisation_horizon
