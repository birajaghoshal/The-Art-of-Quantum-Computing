# Toy RSA with two small primes (completely insecure!)
from math import gcd

p, q = 53, 71                  # Alice's secret primes
n = p * q                      # public modulus
phi = (p - 1) * (q - 1)        # Euler's totient of n
e = 17                         # public exponent
assert gcd(e, phi) == 1
d = pow(e, -1, phi)            # private exponent: e*d = 1 mod phi
print(f"public key  (n, e) = ({n}, {e})")
print(f"private key d      = {d}")

m = 2026                       # Bob's message, a number below n
c = pow(m, e, n)               # encrypt with the public key
print(f"message {m} -> ciphertext {c}")
print(f"Alice decrypts     -> {pow(c, d, n)}")

# Eve only knows (n, e). Factoring n gives her everything.
f = next(k for k in range(2, n) if n % k == 0)
d_eve = pow(e, -1, (f - 1) * (n // f - 1))
print(f"Eve factors n = {f} x {n // f}, finds d = {d_eve}")
print(f"Eve decrypts       -> {pow(c, d_eve, n)}")
