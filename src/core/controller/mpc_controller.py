import logging
import time
from decimal import Decimal
from typing import List

from scipy.integrate import quad
from scipy.optimize import minimize

from .controller import ControlAction
from .objective.control_objective import ControlObjective
from .controller import Controller
from .problem.mpc_problem import MPCProblem

from ..model.model import Model
from ..simulation.world_state import WorldState

import numpy as np


def current_milli_time():
    return time.time_ns() // 1_000_000


class TookTooLong(Exception):
    def __init__(self, x):
        self.x = x


class MinimizeStopper(object):
    def __init__(self, max_sec):
        self.max_milli = max_sec * 1000
        self.start = current_milli_time()

    def __call__(self, xk):
        elapsed = current_milli_time() - self.start
        if elapsed > self.max_milli:
            raise TookTooLong(xk)


class MPCController(Controller):

    def __init__(self, mpc_problem: MPCProblem, model: Model, fps: int = 1):
        super().__init__(mpc_problem, fps)
        self.mpc_problem = mpc_problem
        self.model = model

    def calculate_control_actions(self, time_delta: Decimal, latest_world: WorldState) -> List[ControlAction]:
        logging.debug("================================= Controller starting step.")

        initial_guess = [float(v) for k, v in latest_world.variables.items() if k in latest_world.mvs]
        logging.debug("Optimization initial guess %s", initial_guess)

        # min objective function
        result = None
        try:
            returned = minimize(cost_function, np.array(initial_guess),
                                args=(latest_world, self.model, self.mpc_problem),
                                tol=0.1,
                                options={"maxiter": 15}, callback=MinimizeStopper(1))  # todo specify constraints
            logging.debug("Optimization result %s", returned)
            result = returned.x.astype(Decimal)
        except TookTooLong as e:
            result = e.x.astype(Decimal)

        # print("\n\nOptimization result {}\n\n".format(returned))
        # TODO  simulate, validating constraints are not violated

        new_mvs = dict(zip(latest_world.mvs, result))
        logging.debug("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Controller step done.")
        return [ControlAction(k, v) for k, v in new_mvs.items()]


def cost_function(mv_values: np.ndarray, latest_world: WorldState, model: Model,
                  mpc_problem: MPCProblem):
    new_mvs = dict(zip(latest_world.mvs, mv_values.astype(Decimal)))
    logging.debug("\t ========= Cost function being computed for mvs: %s =========", new_mvs)

    # Create world state with same cvs, but different mvs
    updated_control = latest_world.apply_assignment(new_mvs)
    logging.debug("\tupdated world: \n %s", updated_control)

    value = evaluate_world_state(updated_control, model, mpc_problem)
    logging.debug("\tcost of world: %s", value)

    return value


def evaluate_world_state(world_state: WorldState, model: Model, mpc_problem: MPCProblem):
    """
    Evaluates a proposed world state, to see how close to objective we are. Higher is worse
    :param mpc_problem:
    :param model:
    :param world_state:
    :return:
    """
    flags = mpc_problem.active_flags
    weights = mpc_problem.weights
    hz = mpc_problem.optimisation_horizon

    logging.debug("\tEvaluating world.")
    obj = 0
    for cv in world_state.cvs:
        logging.debug("\t\tCV: %s", cv)
        control_objective = mpc_problem.control_objectives[cv]
        integration = quad(f, 0, hz, args=(control_objective, model, world_state))[0]
        logging.debug("\t\tIntegration value: %s", integration)
        obj += float(int(flags[cv])) * float(weights[cv]) * float(integration)
    return obj


def f(t: float, control_objective: ControlObjective, model: Model, world_state: WorldState):
    predicted_world = model.progress(Decimal(t), world_state)
    distance = control_objective.distance_until_satisfied(predicted_world)
    logging.debug("\t\tPredicted world as a result has a distance of %s after %s seconds", distance, t)
    return max(0, distance ** 2)
