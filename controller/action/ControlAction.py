from decimal import Decimal
from typing import Dict

class ControlAction:
    def __init__(self, var: str, value: Decimal):
        self.var = var
        self.value = value

