import numpy as np
import matplotlib.pyplot as plt

def P_eq(r):
    # from Beeler's equilibrium pressure equation
    # radius lower bound: 1.5 nm
    gamma = 1.2    # J/m^2
    A = 4.94 * 1e9 # GPa -> Pa
    B = 0.87 * 1e9 # 1/nm -> 1/m
    return 2 * gamma / r - A * np.exp(-B * r)

r = np.array([i * 1e-9 for i in [1.5, 2, 4, 8, 16, 32, 64, 128]])
P = P_eq(r)

plt.figure(figsize=(5, 4))

plt.plot(r * 1e9, P / 1e9,
         marker='o', label='Beeler et al. (2020)')
plt.plot(r * 1e9, 2.4 / r / 1e9,
         marker='^', ls='--', label='Young-Laplace equation')

plt.xlabel(r'Bubble radius, $R_b$ (nm)')
plt.ylabel(r'Equilibrium bubble pressure, $p_{eq}$ (GPa)')

plt.xlim([1, 200])
plt.xscale('log')

plt.legend()
plt.tight_layout()
plt.savefig('pres_vs_rad.pdf')
