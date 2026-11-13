# A toy learning-with-errors (LWE) bit encryption. NOT secure:
# real ML-KEM uses structured lattices of dimension 512 or more.
import numpy as np

rng = np.random.default_rng(7)
q, n, m = 97, 6, 20                 # modulus, secret length, samples
s = rng.integers(0, q, n)           # secret key
A = rng.integers(0, q, (m, n))      # public random matrix
e = rng.integers(-2, 3, m)          # small errors in {-2..2}
b = (A @ s + e) % q                 # public key is (A, b)

def encrypt(bit):
    pick = rng.integers(0, 2, m)    # random subset of the rows
    u = pick @ A % q
    v = (pick @ b + bit * (q // 2)) % q
    return u, v

def decrypt(u, v):
    noisy = (v - u @ s) % q         # = bit*(q//2) + small error
    return int(min(noisy, q - noisy) > q // 4)

bits = [1, 0, 1, 1, 0, 0, 1, 0]
cts = [encrypt(x) for x in bits]
print("sent:     ", bits)
print("received: ", [decrypt(u, v) for u, v in cts])
u, v = cts[0]
print("first ciphertext: u =", u.tolist(), " v =", int(v))
# v - u.s lands near 0 for a 0 bit and near q//2 = 48 for a 1 bit
print("v - u.s mod q:", [int((v - u @ s) % q) for u, v in cts])
