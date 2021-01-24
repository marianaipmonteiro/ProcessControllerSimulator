import logging
from datetime import datetime

from Console import Console
from simulation.Simulation import Simulation
from examples.cstr.CSTRModel import CSTRModel

if __name__ == "__main__":
    date_str = datetime.now().strftime("%m-%d-%Y-%H-%M")

    format = "%(asctime)s %(levelname)s: %(message)s"
    logging.basicConfig(filename=date_str + '-run.log', format=format, level=logging.INFO, datefmt="%H:%M:%S")

    model = CSTRModel()
    #controller = MPCController(model)
    simulation = Simulation(world_initializer=model, systems={"Physics Model": model})
    simulation.run()

    #vis = Visualizer(simulation)
    #vis.start()

    console = Console(simulation)
    console.trap() #Grab main thread, trapping user input
