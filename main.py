import logging
import os
import sys
import time
from datetime import datetime

from src import Console, load_simulation, WebServer
from src.web.web_visualizer import WebVisualizer


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

    server = WebServer(simulation, debug=True)
    server.start()

    time.sleep(2)

    console = Console(simulation)
    console.trap()  # Grab main thread, trapping user input
