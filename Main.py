import logging
from datetime import datetime

from decimal import Decimal
from Console import Console
from controller.MPCController import MPCController
from controller.objective.AlwaysSatisfiedObjective import AlwaysSatisfiedObjective
from controller.objective.EnvelopeObjective import EnvelopeObjective
from controller.problem.MPCProblem import MPCProblem
from simulation.Simulation import Simulation
from examples.cstr.CSTRModel import CSTRModel
from visualize.Visualizer import Visualizer

if __name__ == "__main__":
    date_str = datetime.now().strftime("%m-%d-%Y-%H-%M")

    format = "%(asctime)s %(levelname)s: %(message)s"
    logging.basicConfig(filename=date_str + '-run.log', format=format, level=logging.INFO, datefmt="%H:%M:%S")

    model = CSTRModel()

    mpc_problem = MPCProblem(
        control_objectives={"Cb": EnvelopeObjective("Cb", Decimal(0.0), Decimal(0.1)),
                            "Tr": AlwaysSatisfiedObjective("Tr")},
        constraints={},
        weights={"Cb": 1.0, "Tr": 1.0},
        active_flags={"Cb": True, "Tr": True},
        prediction_horizon=5,
        optimisation_horizon=5
    )

    controller = MPCController(mpc_problem, model)

    simulation = Simulation(world_initializer=model, systems={"Physics Model": model, "Controller": controller})
    simulation.run()

    vis = Visualizer(simulation)
    vis.start()

    console = Console(simulation)
    console.trap()  # Grab main thread, trapping user input
