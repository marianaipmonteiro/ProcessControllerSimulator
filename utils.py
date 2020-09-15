import cmath
import threading
import time
from decimal import Decimal
from typing import List

from WorldState import WorldState


def quadratic_eq(a: Decimal,b: Decimal, c: Decimal) -> (Decimal, Decimal):
    d = (b**2) - (4*a*c)
    sqrt_d = Decimal(cmath.sqrt(d).real)
    sol1 = Decimal((-b - sqrt_d) / (2 * a))
    sol2 = Decimal((-b + sqrt_d) / (2 * a))
    return sol1, sol2

def wait_for_world_initialization(lock: threading.Lock, world_states: List[WorldState]):
        while not True:
            lock.acquire(True)
            if len(world_states) != 0:
                break
            time.sleep(1)
            lock.release()
