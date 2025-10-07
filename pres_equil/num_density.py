import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

def Pres(v):
    T = 400

    A = 1
    B = 14.625 + 54597.728 / T - 386.344 / T**2
    C = 2968.616 + 2938.01 / T - 84.545 / T**2
    D = 705527.001 + 53.609 / T + 421.138 / T**2
    p = 8.3145 * T / v * (A + B/v + C/v**2 + D/v**3)

    return p # MPa

def eqz(v, P):
    return Pres(v) * 1e6 - P

def P_eq(r):
    # from Beeler's equilibrium pressure equation
    # radius lower bound: 1.5 nm
    gamma = 1.2    # J/m^2
    A = 4.94 * 1e9 # GPa -> Pa
    B = 0.87 * 1e9 # 1/nm -> 1/m
    return 2 * gamma / r - A * np.exp(-B * r)

r = np.array([i * 1e-9 for i in [1.5, 2, 4, 8, 16, 32, 64, 128]])
P1 = P_eq(r)
P2 = 2.4 / r

# molar volume (cm^3/mol)
v1 = []
v2 = []
for p1, p2 in zip(P1, P2):
    g = 1
    v1.append(fsolve(eqz, g, args=(p1))[0])
    v2.append(fsolve(eqz, g, args=(p2))[0])

# Xe/vac ratio
# 11.86 is based on 400 K
r1 = [11.86 / i for i in v1]
r2 = [11.86 / i for i in v2]

# U-10Mo is 0.05 ang^-3
print('Beeler EOS: ', [float(0.05 * i) for i in r1])
print('Young-Laplace: ', [float(0.05 * i) for i in r2])

# number density
n1 = [5e28 * i for i in r1]
n2 = [5e28 * i for i in r2]

plt.figure(figsize=(5, 4))

plt.plot(r * 1e9, n1,
         marker='o', label='Beeler et al. (2020)')
plt.plot(r * 1e9, n2,
         marker='^', ls='--', label='Young-Laplace equation')

plt.xlabel(r'Bubble radius, $R_b$ (nm)')
# plt.ylabel(r'Molar volume, $v$ (cm$^3$/mol)')
# plt.ylabel(r'Xe/vac ratio, $\phi$')
plt.ylabel(r'Number density, $n$ (m$^{-3}$)')

plt.xlim([1, 200])
plt.xscale('log')

plt.legend()
plt.tight_layout()
plt.savefig('n_vs_rad.pdf')
