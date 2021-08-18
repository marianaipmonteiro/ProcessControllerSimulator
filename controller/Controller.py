import logging
import time
from decimal import Decimal
from typing import List, Dict

from controller.action.ControlAction import ControlAction
from controller.problem.ControlProblem import ControlProblem
from simulation.SimulatedSystem import SimulatedSystem
from simulation.WorldState import WorldState


def current_milli_time():
    return time.time_ns() // 1_000_000


class Controller(SimulatedSystem):
    def __init__(self, control_problem: ControlProblem, fps: int = 5):
        super().__init__(fps)
        self.control_problem = control_problem


    def step(self, time_delta: Decimal):
        start = current_milli_time()
        actions = self.calculate_control_actions(time_delta, self.get_latest_world())
        end = current_milli_time()
        logging.debug("Finished calculating control actions! Took {}s".format((end-start)/1000))
        actions_dict = dict([(a.var, a.value) for a in actions])
        self.apply_changes_to_latest_world(actions_dict)


    def calculate_control_actions(self, time_delta: Decimal, latest_world: WorldState) -> List[ControlAction]:
        raise Exception(
            "Controller " + str(self.__class__) + " does not implement calculate_control_actions() function")
