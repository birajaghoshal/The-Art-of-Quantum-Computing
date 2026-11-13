import numpy as np

N = 8
omega = np.exp(2j * np.pi / N)           # 8th root of unity
F = np.array([[omega ** (j * k) for j in range(N)]
              for k in range(N)]) / np.sqrt(N)   # QFT matrix

x = np.array([3, 1, 0, 2, 0, 1, 1, 0], dtype=complex)
x /= np.linalg.norm(x)                   # a valid quantum state

qft = F @ x
fwd = np.fft.fft(x, norm="ortho")        # numpy: minus sign
inv = np.fft.ifft(x, norm="ortho")       # numpy: plus sign

np.set_printoptions(precision=3, suppress=True)
print("F @ x       :", qft[:3])
print("fft(ortho)  :", fwd[:3])
print("ifft(ortho) :", inv[:3])
print("F @ x == ifft(x, ortho):", np.allclose(qft, inv))
print("F @ x == fft(x, ortho) :", np.allclose(qft, fwd))
print("F is unitary:", np.allclose(F.conj().T @ F, np.eye(N)))
print("norm after F:", round(float(np.linalg.norm(qft)), 6))
