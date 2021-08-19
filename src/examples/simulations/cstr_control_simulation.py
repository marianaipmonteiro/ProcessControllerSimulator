from decimal import Decimal

from src.core import Simulation, MPCProblem, EnvelopeObjective, AlwaysSatisfiedObjective, MPCController
from ..models.cstr_model import CSTRModel


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
