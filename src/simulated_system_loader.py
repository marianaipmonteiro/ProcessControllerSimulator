import importlib

from src.core.controller.controller import Controller
from src.core.model.model import Model
from src.core.simulation.simulated_system import SimulatedSystem
from src.core.simulation.simulation import Simulation
from src.core.simulation.world_initializer import WorldInitializer


def load_simulation(path: str) -> Simulation:
    tokens = path.split(".")
    name = tokens[-1]
    mod = importlib.import_module(".".join(tokens[0:-1]), ".")

    clazz = mod.__getattribute__(name)
    instance = clazz()

    if not isinstance(instance, Simulation):
        raise Exception("Requested loading Simulation {}, which is not a Simulation".format(path))

    return instance

def load_system(path: str, args) -> SimulatedSystem:
    name = path.split(".")[-1]
    mod = importlib.import_module(path, ".")

    clazz = mod.__getattribute__(name)
    instance = clazz(**args)

    if not isinstance(instance, SimulatedSystem):
        raise Exception("Requested loading SimulatedSystem {}, which is not a SimulatedSystem".format(path))

    return instance

def load_model(path: str, **kwargs) -> Model:
    instance = load_system(path, kwargs)
    if not isinstance(instance, Model):
        raise Exception("Requested loading Model {}, which is not a Model".format(path))
    return instance

def load_controller(path: str, **kwargs) -> Controller:
    instance = load_system(path, kwargs)
    if not isinstance(instance, Controller):
        raise Exception("Requested loading Controller {}, which is not a Controller".format(path))
    return instance

def load_world_initializer(path: str, **kwargs) -> WorldInitializer:
    instance = load_system(path, kwargs)
    if not isinstance(instance, WorldInitializer):
        raise Exception("Requested loading WorldInitializer {}, which is not a WorldInitializer".format(path))
    return instance
