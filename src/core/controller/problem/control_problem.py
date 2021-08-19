from typing import Dict

from src.core.controller.constraint.constraint import Constraint
from src.core.controller.objective.control_objective import ControlObjective


class ControlProblem:

    def __init__(self, control_objectives: Dict[str, ControlObjective], constraints: Dict[str, Constraint],
                 real_time: bool = True):
        self.control_objectives = control_objectives
        self.constraints = constraints
        self.real_time = real_time
