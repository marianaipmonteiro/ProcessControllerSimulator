import logging

from Simulation import Simulation
from examples.cstr.CSTRModel import CSTRModel

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    model = CSTRModel()
    simulation = Simulation(None, model, 1, 1)
    simulation.run()




