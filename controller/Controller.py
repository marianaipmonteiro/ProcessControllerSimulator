from decimal import Decimal
from typing import List, Dict

from controller.action.ControlAction import ControlAction
from controller.problem.ControlProblem import ControlProblem
from simulation.SimulatedSystem import SimulatedSystem
from controller.objective.ControlObjective import ControlObjective
from simulation.WorldState import WorldState


class Controller(SimulatedSystem):
    def __init__(self, control_problem: ControlProblem, fps: int = 5):
        super().__init__(fps)
        self.control_problem = control_problem

    def step(self, time_delta: Decimal):
        actions = self.calculate_control_actions(time_delta, self.get_latest_world())
        actions_dict = dict([(a.var, a.value) for a in actions])
        self.apply_changes_to_latest_world(actions_dict)

    def calculate_control_actions(self, time_delta: Decimal, latest_world: WorldState) -> List[ControlAction]:
        raise Exception(
            "Controller " + str(self.__class__) + " does not implement calculate_control_actions() function")
