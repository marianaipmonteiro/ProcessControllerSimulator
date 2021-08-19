from decimal import Decimal


class ControlAction:
    def __init__(self, var: str, value: Decimal):
        self.var = var
        self.value = value
