from typing import Dict

from controller.constraint.Constraint import Constraint
from controller.objective.ControlObjective import ControlObjective


class ControlProblem:

    def __init__(self, control_objectives : Dict[str, ControlObjective], constraints : Dict[str, Constraint]):
        self.control_objectives = control_objectives
        self.constraints = constraints