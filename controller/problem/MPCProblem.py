from typing import Dict

from controller.constraint.Constraint import Constraint
from controller.objective.ControlObjective import ControlObjective
from controller.problem.ControlProblem import ControlProblem


class MPCProblem(ControlProblem):
    def __init__(self, control_objectives: Dict[str, ControlObjective], constraints: Dict[str, Constraint],
                 weight: Dict[str, float], active_flags: Dict[str, bool], prediction_horizon: float,
                 optimisation_horizon: float):
        super().__init__(control_objectives, constraints)
        self.weight_coefficients = weight
        self.prediction_horizon = prediction_horizon
        self.active_flags = active_flags
        self.optimisation_horizon = optimisation_horizon
