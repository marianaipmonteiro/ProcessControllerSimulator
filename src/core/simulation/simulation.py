import logging
import threading
from typing import List, Dict

from src.core.simulation.world_initializer import WorldInitializer
from src.core.simulation.world_state import WorldState
from src.core.simulation.simulated_system import SimulatedSystem


class Simulation:
    def __init__(self, world_initializer: WorldInitializer, systems: Dict[str, SimulatedSystem],
                 time_multiplier: int = 10):
        self.world_states: List[WorldState] = []
        self.world_states_lock = threading.Lock()
        self.systems = systems
        self.world_initializer = world_initializer
        self.time_multiplier = time_multiplier
        self.running = False
        logging.info("Simulation created:\n %s", self)

    def add_system(self, name: str, system: SimulatedSystem):
        self.systems[name] = system
        system.run(self.world_states, self.world_states_lock, self.time_multiplier)

    def remove_system(self, name: str):
        system = self.systems.pop(name)
        system.stop_system()

    def run(self):
        self.running = True
        # Setup initial world
        initial_world = self.world_initializer.create_initial_world()
        self.world_states.append(initial_world)

        # Start systems
        for name, system in self.systems.items():
            system.run(self.world_states, self.world_states_lock, self.time_multiplier)
            logging.info("Starting system %s!", name)

    def stop(self):
        for name, system in self.systems.items():
            system.stop_system()
        self.running = False

    def is_running(self) -> bool:
        return self.running

    def __str__(self):
        res = "Simulation{\n"
        res += "\tTime Multiplier -> {},\n".format(self.time_multiplier)
        res += "\tWorldInitializer -> {},\n".format(self.world_initializer)
        res += "\tSystems = {\n"
        for key in self.systems:
            res += "\t\t\"" + key + "\" -> " + str(self.systems[key]) + ",\n"
        res += "\t}\n"
        res += "}\n"
        return res
