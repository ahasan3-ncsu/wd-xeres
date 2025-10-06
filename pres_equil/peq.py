import numpy as np
import matplotlib.pyplot as plt

def P_eq(r):
    # from Beeler's equilibrium pressure equation
    # radius lower bound: 1.5 nm
    gamma = 1.2    # J/m^2
    A = 4.94 * 1e9 # GPa -> Pa
    B = 0.87 * 1e9 # 1/nm -> 1/m
    return 2 * gamma / r - A * np.exp(-B * r)

# r = np.linspace(1.5e-9, 128e-9, 100)
r = [i * 1e-9 for i in [1.5, 2, 4, 8, 16, 32, 64, 128]]
r = np.array(r)
P = P_eq(r)

plt.plot(r, P, marker='o', label='Beeler et al. (2020)')
plt.plot(r, 2.4/r, marker='^', label='Young-Laplace equation')

plt.xscale('log')
plt.legend()
plt.show()
