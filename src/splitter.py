import secrets
import hashlib
from const import (
    fm,
    fm_bmp,
)


def rnd_scalar(fm: int):
    return secrets.randbelow(fm)


def hash_to_scalar(msg: int, fm: int):
    return (
        int.from_bytes(hashlib.sha3_256(str(msg).encode()).digest(), "big")
        % fm
    )


# s: secret, n: number of shares, k: threadshold
def generate_share(s: int, n: int, k: int, fm: int):    
    coefficients = [s]
    for i in range(1, k):
        tmp = rnd_scalar(fm)
        coefficients.append(tmp)
    
    def f(x):
        func = sum(coef * x**j for j, coef in enumerate(coefficients))
        return func
    
    shares = [f(x) for x in range(1, n + 1)]
    return shares


def generate_share_2(s: int, n: int, k: int, rnd: list):
    coefficients = [s]
    coefficients += rnd
    
    def f(x):
        func = sum(coef * x**j for j, coef in enumerate(coefficients))
        return func
    
    shares = [f(x) for x in range(1, n + 1)]
    return shares
