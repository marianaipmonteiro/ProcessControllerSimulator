from decimal import Decimal
from typing import Dict


class ControlAction:
    def __init__(self, assignment: Dict[str, Decimal]):
        self.assignment = assignment

