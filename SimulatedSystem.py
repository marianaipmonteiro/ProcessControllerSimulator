import threading
import time
from decimal import Decimal
from typing import List, Callable

from Simulation import RunningFlag
from WorldState import WorldState


class SimulatedSystem:
    def __init__(self):
        pass

    def simulate_system(self, fps: int, world_states: List[WorldState], lock: threading.Lock, running: RunningFlag):
        ms_per_update = Decimal(1000 / fps)
        current_milli_time = lambda: Decimal(round(time.time() * 1000))
        previous = current_milli_time()
        lag = Decimal(0.0)

        while (running.is_running()):
            current = current_milli_time()
            elapsed = Decimal(current - previous)
            previous = current
            lag += elapsed

            while lag >= ms_per_update:
                self.simulation_step(lock, ms_per_update / 1000 / 60, world_states)
                lag -= ms_per_update

            time.sleep(ms_per_update / 1000 / 4)


    def simulation_step(self, lock, time_delta, world_states):
        lock.acquire(True)
        self.step(time_delta, world_states)
        lock.release()


    def step(self, time_delta, world_states):
        raise Exception("Simulated System " + str(self.__class__) + " does not implement step() function")
