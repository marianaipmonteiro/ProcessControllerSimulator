import threading
import time
from decimal import Decimal
from typing import List

from simulation.WorldState import WorldState
from RunningFlag import RunningFlag


class SimulatedSystem:
    def __init__(self, fps: int = 5):
        self.fps = fps

    def run(self, world_states: List[WorldState], lock: threading.Lock, running: RunningFlag, time_multiplier: int):
        """
        Runs the SimulatedSystem.
        Each SimulatedSystem is run on a separate thread.
        :param world_states: The states of the world produced until now.
        :param lock: The lock protecting world_states.
        :param running: A flag indicating whether the simulation is still running.
        """
        threading.Thread(target=self.simulate_system, args=(self.fps, world_states, lock, running, time_multiplier)).start()

    def simulate_system(self, fps: int, world_states: List[WorldState], lock: threading.Lock, running: RunningFlag, time_multiplier: int):
        ms_per_update = Decimal(1000 / fps)
        current_milli_time = lambda: Decimal(round(time.time() * 1000))
        previous = current_milli_time()
        lag = Decimal(0.0)

        while running.is_running():
            current = current_milli_time()
            elapsed = Decimal(current - previous)
            previous = current
            lag += elapsed

            while lag >= ms_per_update:
                self.simulation_step(lock, ms_per_update / 1000 / 60 * time_multiplier, world_states)
                lag -= ms_per_update

            time.sleep(ms_per_update / 1000 / 4)

    def simulation_step(self, lock, time_delta, world_states):
        lock.acquire()
        self.step(time_delta, world_states)
        lock.release()

    def step(self, time_delta, world_states):
        raise Exception("Simulated System " + str(self.__class__) + " does not implement step() function")

    def __str__(self):
        return self.__class__.__name__
