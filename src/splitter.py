import sympy
import secrets
import hashlib
from const import (
    fm,
)


def rnd_scalar():
    return secrets.randbelow(fm)


def hash_to_scalar(msg):
    return (
        int.from_bytes(hashlib.sha3_256(str(msg).encode()).digest(), "big")
        % fm
    )


# s: secret, n: number of shares, k: threadshold
def generate_share(s: int, n: int, k: int):    
    coefficients = [s]
    for i in range(1, k):
        # tmp = hash_to_scalar(f"hash_to_scalar:{s}:{i*rnd_scalar()}") * rnd_scalar() % fm
        tmp = rnd_scalar()
        coefficients.append(tmp)
    
    def f(x):
        # func = sum(coef * pow(x, j, fm) for j, coef in enumerate(coefficients)) % fm
        func = sum(coef * pow(x, j, fm) for j, coef in enumerate(coefficients))
        return func

    
    shares = [f(x) for x in range(1, n + 1)]
    return shares
