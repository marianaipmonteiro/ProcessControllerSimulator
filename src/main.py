import logging
import os
import sys
from datetime import datetime

from console import Console
from simulated_system_loader import load_simulation
from web import WebVisualizer


def setup_logs():
    date_str = datetime.now().strftime("%m-%d-%Y-%H-%M")
    logs_dir = "../logs/"
    try:
        os.makedirs(logs_dir)
    except FileExistsError:
        # directory already exists
        pass

    fmt = "%(asctime)s %(levelname)s: %(message)s"
    logging.basicConfig(filename=logs_dir + date_str + '-run.log', format=fmt, level=logging.DEBUG,
                        datefmt="%H:%M:%S")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise Exception("Args may only contain path to simulation")

    setup_logs()

    path_to_sim = sys.argv[1]
    simulation = load_simulation(path_to_sim)
    simulation.run()

    vis = WebVisualizer(simulation)
    vis.start()

    console = Console(simulation)
    console.trap()  # Grab main thread, trapping user input
