import sympy
from const import (
    fm,
)

def lagrange(x: int, shares: list):
    result = 0
    for i in range(len(shares)):
        elc = lagrange_coef(x, i, shares)
        tmp = (shares[i] * elc)
        result = (result + tmp) % fm
    return result


def lagrange_coef(x: int, i: int, shares: list):
    result = 1
    for j in range(len(shares)):
        if i != j:
            result *= (x - j - 1) * sympy.mod_inverse(i - j, fm)
            result %= fm
    return result
