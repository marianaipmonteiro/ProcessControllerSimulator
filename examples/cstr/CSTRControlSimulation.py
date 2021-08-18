from decimal import Decimal

from controller.MPCController import MPCController
from controller.objective.AlwaysSatisfiedObjective import AlwaysSatisfiedObjective
from controller.objective.EnvelopeObjective import EnvelopeObjective
from controller.problem.MPCProblem import MPCProblem
from examples.cstr.CSTRModel import CSTRModel
from simulation.Simulation import Simulation


class CSTRControlSimulation(Simulation):
    def __init__(self):
        model = CSTRModel()

        mpc_problem = MPCProblem(
            control_objectives={"Cb": EnvelopeObjective("Cb", Decimal(1), Decimal(1)),
                                "Tr": AlwaysSatisfiedObjective("Tr")},
            constraints={},
            weights={"Cb": 400.0, "Tr": 1.0},
            active_flags={"Cb": True, "Tr": True},
            prediction_horizon=5,
            optimisation_horizon=5
        )

        controller = MPCController(mpc_problem, model)

        super().__init__(world_initializer=model, systems={"Physics Model": model, "Controller": controller})
