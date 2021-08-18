import datetime
from copy import deepcopy
from decimal import *
from typing import Dict, List


class WorldState:

    def __init__(self, constants: Dict[str, Decimal], variables: Dict[str, Decimal], mvs: List[str], cvs: List[str]):
        getcontext().prec = 10 # TODO make configurable
        for key in constants.keys():
            constants[key] = Decimal(constants[key])
            setattr(self, key, constants[key])
        for key in variables.keys():
            variables[key] = Decimal(variables[key])
            setattr(self, key, variables[key])

        self.constants = constants
        self.variables = variables
        self.mvs = mvs
        self.cvs = cvs

        self.wall_clock_time = datetime.datetime.now()

    def __str__(self):
        res = "WorldState{\n"
        res += "\tConstants{\n"
        for key in self.constants:
            res += "\t\t" + key + " -> " + str(self.constants[key]) + ",\n"
        res += "\t}\n"
        res += "\tVariables{\n"
        for key in self.variables:
            res += "\t\t" + key + " -> " + str(self.variables[key]) + ",\n"
        res += "\t}\n"
        res += "\tManipulated Variables=" + str(self.mvs)
        res += "\tControlled Variables=" + str(self.cvs)
        #res += "\tDisturbance Variables=" + str(self.dvs)
        res += "}\n"
        return res

    def __getitem__(self, item):
        return getattr(self, item)

    def copy_except(self, key, new_val):
        vars_copy = deepcopy(self.variables)
        vars_copy[key] = new_val
        copy = WorldState(self.constants, vars_copy, self.mvs, self.cvs)
        return copy

    def apply_assignment(self, updates: Dict[str, Decimal]):
        vars_copy = deepcopy(self.variables)
        for key, val in updates.items():
            vars_copy[key] = val
        copy = WorldState(self.constants, vars_copy, self.mvs, self.cvs)
        return copy

    def apply_increments(self, increments: Dict[str, Decimal]):
        vars_copy = deepcopy(self.variables)
        for key, val in increments.items():
            vars_copy[key] = self.variables[key] + val
        copy = WorldState(self.constants, vars_copy, self.mvs, self.cvs)
        return copy

