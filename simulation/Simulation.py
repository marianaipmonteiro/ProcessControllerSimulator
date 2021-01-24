import logging
import threading
from typing import List, Dict

from RunningFlag import RunningFlag
from simulation.SimulatedSystem import SimulatedSystem
from simulation.WorldInitializer import WorldInitializer
from simulation.WorldState import WorldState


class Simulation:
    def __init__(self, world_initializer: WorldInitializer, systems: Dict[str, SimulatedSystem], time_multiplier: int = 10):
        self.world_states: List[WorldState] = []
        self.world_states_lock = threading.Lock()
        self.running = RunningFlag()
        self.systems = systems
        self.world_initializer = world_initializer
        self.time_multiplier = time_multiplier
        logging.info("Simulation created:\n %s", self)

    def run(self):
        #Setup initial world
        initial_world = self.world_initializer.create_initial_world()
        self.world_states.append(initial_world)

        #Start systems
        for name, system in self.systems.items():
            system.run(self.world_states, self.world_states_lock, self.running, self.time_multiplier)
            logging.info("Starting system %s!", name)

    def __str__(self):
        res = "Simulation{\n"
        res += "\tTime Multiplier -> {}\n".format(self.time_multiplier)
        res += "\tWorldInitializer -> {}\n".format(self.world_initializer)
        res += "\tSystems = {\n"
        for key in self.systems:
            res += "\t\t" + key + " -> " + str(self.systems[key]) + ",\n"
        res += "\t}\n"
        res += "}\n"
        return res