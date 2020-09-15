import threading
import time
from typing import List, Dict

from SimulatedSystem import SimulatedSystem
from Simulation import RunningFlag
from WorldState import WorldState
from controller.ControlAction import ControlAction
from controller.ControlObjective import ControlObjective
from model.Model import Model
from utils import wait_for_world_initialization


class Controller(SimulatedSystem):
    def __init__(self, control_objectives: Dict[str, ControlObjective], model: Model):
        super().__init__()
        self.control_objectives = control_objectives

    def run(self, controller_fps: int, world_states: List[WorldState], lock: threading.Lock, running: RunningFlag):
        # Wait for world initialization
        wait_for_world_initialization(lock, world_states)

        threading.Thread(target=self.simulate_system, args=(controller_fps, world_states, lock, running)).start()

    def step(self, time_delta, world_states):
        pass
