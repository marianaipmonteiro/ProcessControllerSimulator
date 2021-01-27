from typing import Dict

from controller.constraint.Constraint import Constraint
from controller.objective.ControlObjective import ControlObjective
from controller.problem.ControlProblem import ControlProblem


class MPCProblem(ControlProblem):
    """
    Specifies all the parameters of an MPC problem
    """
    def __init__(self, control_objectives: Dict[str, ControlObjective], constraints: Dict[str, Constraint],
                 weights: Dict[str, float], active_flags: Dict[str, bool], prediction_horizon: float,
                 optimisation_horizon: float):
        """
        Creates a new MPCProblem
        :param control_objectives: a dictionary, where key is a cv and value is a control objective for that cv
        :param constraints: a dictionary, where key is a variable and vaue is a constraint on that variable
        :param weights: a dictionary, where key is a cv and value is the optimization weight of that cv
        :param active_flags: a dictionary, where key is a cv and value is a boolean specifying whether that cv should be considered in optimization
        :param prediction_horizon: The horizon up to which the controller predicts the evolution of the system
        :param optimisation_horizon:
        """
        super().__init__(control_objectives, constraints)
        self.weights = weights
        self.prediction_horizon = prediction_horizon
        self.active_flags = active_flags
        self.optimisation_horizon = optimisation_horizon
