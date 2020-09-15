import threading
from datetime import time
from typing import List
import time

from SimulatedSystem import SimulatedSystem
from Simulation import RunningFlag
from WorldState import WorldState
from model.Equation import Equation

from decimal import *

class Model(SimulatedSystem):

    def __init__(self, equations: List[Equation]):
        super().__init__()
        self.equations = equations

    def run(self, fps, world_states: List[WorldState], lock, running: RunningFlag):
        # Prepare initial state
        self.initialize_world(lock, world_states)

        #start thread run equations
        threading.Thread(target=self.simulate_system, args=(fps, world_states, lock, running)).start()

    def initialize_world(self, lock, world_states):
        lock.acquire(True)
        self.initialization(world_states)
        lock.release()

    def initialization(self, world_states):
        """Initialize the world. Synchronized access to world_states"""
        raise Exception("Model does not have initialization() routine implemented.")



