import logging
import sys
from datetime import datetime

from Console import Console
from loading.SimulatedSystemLoader import load_simulation
from visualize.WebVisualizer import WebVisualizer

if __name__ == "__main__":
    date_str = datetime.now().strftime("%m-%d-%Y-%H-%M")

    format = "%(asctime)s %(levelname)s: %(message)s"
    logging.basicConfig(filename=date_str + '-run.log', format=format, level=logging.DEBUG, datefmt="%H:%M:%S")

    if len(sys.argv) != 2:
        raise Exception("Args includes only path to simulation")

    path_to_sim = sys.argv[1]
    simulation = load_simulation(path_to_sim)
    simulation.run()

    vis = WebVisualizer(simulation)
    vis.start()

    console = Console(simulation)
    console.trap()  # Grab main thread, trapping user input
