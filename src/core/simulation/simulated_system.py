import threading
import time
from decimal import Decimal
from typing import List, Dict

from src.core.simulation.world_state import WorldState


class SimulatedSystem:
    def __init__(self, fps: int = 5):
        self.world_states = None
        self.lock = None
        self.running = False
        self.time_multiplier = None
        self.fps = fps

    def run(self, world_states: List[WorldState], lock: threading.Lock, time_multiplier: int):
        """
        Runs the SimulatedSystem.
        Each SimulatedSystem is run on a separate thread.
        :param time_multiplier:
        :param world_states: The states of the world produced until now.
        :param lock: The lock protecting world_states.
        """
        self.world_states = world_states
        self.lock = lock
        self.time_multiplier = time_multiplier
        threading.Thread(target=self.simulate_system).start()

    def simulate_system(self):
        self.running = True
        ms_per_update = Decimal(1000 / self.fps)
        current_milli_time = lambda: Decimal(round(time.time() * 1000))
        previous = current_milli_time()
        lag = Decimal(0.0)

        while self.running:
            current = current_milli_time()
            elapsed = Decimal(current - previous)
            previous = current
            lag += elapsed

            while lag >= ms_per_update:
                self.step(ms_per_update / 1000 / 60 * self.time_multiplier)
                lag -= ms_per_update

            time.sleep(float(ms_per_update / 1000 / 4))  # Sleep this thread for a period shorter than update period

    def stop_system(self):
        self.running = False  # TODO maybe need some sync

    def get_latest_world(self) -> WorldState:
        self.lock.acquire()
        latest_world = self.world_states[-1]
        self.lock.release()
        return latest_world

    def get_all_world_states(self) -> List[WorldState]:
        self.lock.acquire()
        copy = self.world_states.copy()
        self.lock.release()
        return copy

    def append_world(self, world: WorldState):
        self.lock.acquire()
        self.world_states.append(world)
        self.lock.release()

    def apply_changes_to_latest_world(self, dict: Dict[str, Decimal]):
        self.lock.acquire()
        latest_world: WorldState = self.world_states[-1]
        self.world_states.append(latest_world.apply_assignment(dict))
        self.lock.release()

    def apply_incremental_changes_to_latest_world(self, dict: Dict[str, Decimal]):
        self.lock.acquire()
        latest_world: WorldState = self.world_states[-1]
        self.world_states.append(latest_world.apply_increments(dict))
        self.lock.release()

    def step(self, time_delta: Decimal):
        raise Exception("Simulated System " + str(self.__class__) + " does not implement step() function")

    def __str__(self):
        return self.__class__.__name__
