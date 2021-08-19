from decimal import Decimal
from random import uniform
from src.core import SimulatedSystem


class RandomPeriodicDisturbance(SimulatedSystem):
    def __init__(self, fps=5, variable="Cb", min_disturbance=0.0, max_disturbance=5.0):
        super().__init__(int(fps))
        self.variable = variable
        self.min_disturbance = float(min_disturbance)
        self.max_disturbance = float(max_disturbance)

    def step(self, time_delta: Decimal):
        increment = Decimal(uniform(self.min_disturbance, self.max_disturbance))
        self.apply_incremental_changes_to_latest_world({self.variable: increment})
