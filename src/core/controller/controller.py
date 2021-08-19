from decimal import Decimal
from typing import List

from .action.control_action import ControlAction
from .problem.control_problem import ControlProblem
from ..simulation.simulated_system import SimulatedSystem
from ..simulation.world_state import WorldState


class Controller(SimulatedSystem):
    def __init__(self, control_problem: ControlProblem, fps: int = 5):
        super().__init__(fps)
        self.control_problem = control_problem

    def step(self, time_delta: Decimal):
        if self.control_problem.real_time:
            self._step(time_delta)
        else:
            # If problem is not real time, acquire lock to stop the world during controller step
            self.lock.acquire()
            self._step(time_delta)
            self.lock.release()

    def _step(self, time_delta):
        actions = self.calculate_control_actions(time_delta, self.get_latest_world())
        actions_dict = dict([(a.var, a.value) for a in actions])
        self.apply_changes_to_latest_world(actions_dict)

    def calculate_control_actions(self, time_delta: Decimal, latest_world: WorldState) -> List[ControlAction]:
        raise Exception(
            "Controller " + str(self.__class__) + " does not implement calculate_control_actions() function")
