from fractions import Fraction
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
            result *= Fraction(x - j - 1, i - j)
    return int(result)
