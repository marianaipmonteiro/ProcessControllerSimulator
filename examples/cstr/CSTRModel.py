import math
from decimal import Decimal
from typing import Dict

from WorldState import WorldState
from model import Model, Equation
from model.StaticInitializedModel import StaticInitializedModel
from utils import quadratic_eq


class CSTRModel(StaticInitializedModel):

    def __init__(self):
       equations = []
       equations.append(ReactionRate())
       equations.append(MassBalanceA())
       equations.append(MassBalanceB())
       equations.append(HeatBalanceTc())
       equations.append(HeatBalanceTr())
       equations.append(ReactionHeat())

       R =8.3144621
       k1_0=2.145 * 10**10
       k2_0=2.145 * 10**10
       k3_0=1.5072 * 10**8
       ca0=5.1
       cb0=0
       tr0=387.05
       h1 = -4200
       h2 = -11000
       h3 = -41850

       initial_world_state = WorldState(
                                constants={"k1_0" : k1_0, #min-1
                                "k2_0":k2_0, #min-1
                                "k3_0":k3_0, #min-1
                                "R":R, # KJ kg-1 K-1
                                "E_1":9758.3*R, # K
                                "E_2":9758.3*R, # K
                                "E_3":8560.0*R, # K
                                "h1": h1, # kJ kmol-1
                                "h2": h2, # kJ kmol-1
                                "h3": h3, # kJ kmol-1
                                "Vr":0.01, # m3
                                "rho":934.2, # kg m -3
                                "CpR":3.01, # kJ kg-1 K-1
                                "qr":2.365 * 10**-3, # m3 min-1
                                "CpC":2.0, # kJ kg-1 K-1
                                "Qc":-18.5583, # kJ min-1
                                "U":67.2, # kJ min-1 m-2 K-1
                                "Ar":0.215, # m2
                                "Ca_0":ca0, # kmol m-3
                                "Cb_0":cb0,  # kmol m-3
                                "Tr_0":tr0, # K
                                "mc":5}, # kg

                                variables={"k1":k1_0,
                                "k2":k2_0, #min-1
                                "k3":k3_0, #min-1
                                "Ca":ca0, # kmol m-3
                                "Cb":cb0, # kmol m-3
                                "Tr":tr0, # K
                                "Tc":0, # K
                                "hR": 0   # kJ kmol-1
                                           },

                                mvs=[
                                "Ca",
                                "Tc"
                                ],

                                cvs=[
                                "Cb",
                                "Tr"
                                ]
                                )
       super().__init__(equations, initial_world_state)

class ReactionRate(Equation.Equation):
    def initialize(self, ws: WorldState) -> Dict[str, Decimal]:
        k1 = ws.k1_0 * (- ws.E_1 / (ws.R * ws.Tr_0)).exp()
        k2 = ws.k2_0 * (- ws.E_2 / (ws.R * ws.Tr_0)).exp()
        k3 = ws.k3_0 * (- ws.E_3 / (ws.R * ws.Tr_0)).exp()

        return {"k1": k1,
                "k2": k2,
                "k3": k3}

    def apply(self, ws: WorldState, time_delta: Decimal) -> Dict[str, Decimal]:
        k1 = ws.k1_0 * ( - ws.E_1/ (ws.R * ws.Tr)).exp()
        k2 = ws.k2_0 * ( - ws.E_2/ (ws.R * ws.Tr)).exp()
        k3 = ws.k3_0 * ( - ws.E_3/ (ws.R * ws.Tr)).exp()

        return {"k1": k1,
            "k2": k2,
            "k3": k3}

class MassBalanceA(Equation.Equation):

    def initialize(self, ws: WorldState) -> Dict[str, Decimal]:
        sol1, sol2 = quadratic_eq(ws.k3,ws.qr/ws.Vr + ws.k1, - ws.qr/ ws.Vr * ws.Ca_0 )
        return {"Ca" : sol1 if sol1 > 0 else sol2}

    def apply(self, ws: WorldState, time_delta: Decimal) -> Dict[str, Decimal]:
        Ca_delta = (ws.qr/ws.Vr * (ws.Ca_0-ws.Ca) - ws.k1 * ws.Ca - ws.k3 * ws.Ca ** 2) * time_delta
        return {"Ca": ws.Ca + Ca_delta}

class MassBalanceB(Equation.Equation):
    def initialize(self, ws: WorldState) -> Dict[str, Decimal]:
        sol = -ws.k1 * ws.Ca / (-ws.qr / ws.Vr -ws.k2)
        return {"Cb": sol}
    def apply(self, ws: WorldState, time_delta: Decimal) -> Dict[str, Decimal]:
        Cb_delta = ( (-ws.qr/ws.Vr * ws.Cb) + ws.k1 * ws.Ca - ws.k2 * ws.Cb ) * time_delta

        return {"Cb": ws.Cb + Cb_delta}


class HeatBalanceTc(Equation.Equation):
    def initialize(self, ws: WorldState) -> Dict[str, Decimal]:
        sol = (ws.Qc + ws.Ar * ws.U * ws.Tr_0)/(ws.Ar * ws.U)
        return {"Tc" : sol}
    def apply(self, ws: WorldState, time_delta: Decimal) -> Dict[str, Decimal]:
        Tc_delta = ((1 / ( ws.mc * ws.CpC ) ) * ( ws.Qc + ws.Ar * ws.U * (ws.Tr - ws.Tc)) ) * time_delta

        return {"Tc": ws.Tc + Tc_delta}

class HeatBalanceTr(Equation.Equation):
    def initialize(self, ws: WorldState) -> Dict[str, Decimal]:

        sol_tr = ((ws.qr * ws.Tr_0)/(ws.Vr) + (1/(ws.rho * ws.CpR) * (-ws.hR + ws.Ar * ws.U * ws.Tc / ws.Vr)))\
                 /\
                 (ws.qr / ws.Vr + ws.Ar * ws.U / (ws.Vr * ws.rho * ws.CpR))
        return {"Tr" : sol_tr}

    def apply(self, ws: WorldState, time_delta: Decimal) -> Dict[str, Decimal]:
        Tr_delta = ( ws.qr/ws.Vr * (ws.Tr_0 - ws.Tr) - (ws.hR/(ws.rho * ws.CpR)) + (ws.Ar * ws.U) / (ws.Vr * ws.rho * ws.CpR) * (ws.Tc - ws.Tr) ) * time_delta

        return {"Tr": ws.Tr + Tr_delta}



class ReactionHeat(Equation.Equation):
    def initialize(self, ws: WorldState) -> Dict[str, Decimal]:

        sol = ws.h1 * ws.k1 * ws.Ca_0 + ws.h2 * ws.k2 * ws.Cb_0 + ws.h3 * ws.k3 * ws.Ca_0 ** 2


        return {"hR" : sol}

    def apply(self, ws: WorldState, time_delta: Decimal) -> Dict[str, Decimal]:
        hR = ws.h1 * ws.k1 * ws.Ca + ws.h2 * ws.k2 * ws.Cb + ws.h3 * ws.k3 * ws.Ca ** 2

        return {"hR": hR}






