import itertools
import numpy as np
from scipy.optimize import fsolve
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt

# bubble radii (m) in my work
Rb = np.array([i * 1e-9 for i in [1, 2, 4, 8, 16, 32, 64, 128]])

# chronological order:
# vdW, Ronchi, Beeler 2020, Beeler 2023, MD

### van der Waals EOS
def vdw_r_n(r):
    k = 1.38e-23 # J/K
    gamma = 1.55 # J/m^2
    B = 8.5e-29  # m^3/atom
    T = 400      # K
    p_eq = 2 * gamma / r
    return 1 / (B + k * T / p_eq)

# number density (1/m^3)
n_vdw = vdw_r_n(Rb)

### Ronchi EOS
ronchi = [
    # (p, v, Z) : (Pascal, cc/mol, unitless)
    (    73e5, 377.4,   0.83),
    (   124e5, 188.7,   0.71),
    (   170e5, 125.8,   0.65),
    (   243e5,  94.3,   0.69),
    (   394e5,  75.5,   0.89),
    (   701e5,  62.9,   1.33),
    (  1284e5,  53.9,   2.08),
    (  2306e5,  47.2,   3.27),
    (  3995e5,  41.9,   5.04),
    (  6659e5,  37.7,   7.56),
    ( 10714e5,  34.3,  11.05),
    ( 16722e5,  31.4,  15.81),
    ( 25467e5,  29.0,  22.23),
    ( 38075e5,  27.0,  30.86),
    ( 56258e5,  25.2,  42.56),
    ( 82826e5,  23.6,  58.74),
    (122880e5,  22.2,  82.02),
    (186960e5,  21.0, 117.86),
    (300848e5,  19.9, 179.68),
    (544531e5,  18.9, 308.95),
]

# make a spline with Ronchi provided data
v_ronchi_train = [i[1] for i in ronchi]
p_ronchi_train = [i[0] for i in ronchi]
ronchi_p_v = PchipInterpolator(p_ronchi_train, v_ronchi_train)

# Young-Laplace (Pa)
p_ronchi = 2 * 1.55 / Rb
# molar volume (cm^3/mol)
v_ronchi = ronchi_p_v(p_ronchi)
# xe/vac ratio (at 400 K)
phi_ronchi = [11.86 / i for i in v_ronchi]
# number density (1/m^3)
n_ronchi = [i * 5e28 for i in phi_ronchi]

### Beeler 2020 EOS
def b2020_v_p(v):
    T = 400

    A = 1
    B = 197.229 + 120307.145 / T + 60.555 / T**2
    C = -22038.723 + 2292.793 / T - 117.564 / T**2
    D = 1030015.045 + 5.200 / T - 280.677 / T**2
    p = 8.3145 * T / v * (A + B/v + C/v**2 + D/v**3)

    return p # MPa

def b2020_eqz(v, P):
    return b2020_v_p(v) * 1e6 - P

def b2020_p_eq(r):
    # from Beeler's equilibrium pressure equation
    # radius lower bound: 1.5 nm
    gamma = 1.2    # J/m^2
    A = 4.94 * 1e9 # GPa -> Pa
    B = 0.87 * 1e9 # 1/nm -> 1/m
    return 2 * gamma / r - A * np.exp(-B * r)

# modified Young-Laplace (Pa)
p_b2020 = b2020_p_eq(Rb)
# molar volume (cm^3/mol)
v_b2020 = []
for p in p_b2020:
    v_b2020.append(fsolve(b2020_eqz, 1, args=(p))[0])
# xe/vac ratio (at 400 K)
phi_b2020 = [11.86 / i for i in v_b2020]
# number density (1/m^3)
n_b2020 = [i * 5e28 for i in phi_b2020]

### Beeler 2023 EOS
def b2023_v_p(v):
    T = 400

    A = 1
    B = 14.625 + 54597.728 / T - 386.344 / T**2
    C = 2968.616 + 2938.01 / T - 84.545 / T**2
    D = 705527.001 + 53.609 / T + 421.138 / T**2
    p = 8.3145 * T / v * (A + B/v + C/v**2 + D/v**3)

    return p # MPa

def b2023_eqz(v, P):
    return b2023_v_p(v) * 1e6 - P

# Young-Laplace (Pa)
p_b2023 = 2 * 1.55 / Rb
# molar volume (cm^3/mol)
v_b2023 = []
for p in p_b2023:
    v_b2023.append(fsolve(b2023_eqz, 1, args=(p))[0])
# xe/vac ratio (at 400 K)
phi_b2023 = [11.86 / i for i in v_b2023]
# number density (1/m^3)
n_b2023 = [i * 5e28 for i in phi_b2023]

### MD simulations with ADP 2023
r_md = [
    # nm
    0.8575,
    1.5435,
    2.2295,
    2.9155,
    3.6015,
    4.2875,
]
phi_md = [
    0.184914842,
    0.193095556,
    0.191923584,
    0.170971228,
    0.158948039,
    0.155015657,
]

# number density (1/m^3)
n_md = [i * 5e28 for i in phi_md]

### Change to 1/angstrom^3 for RustBCA input
num_densities = [n_vdw, n_ronchi, n_b2020, n_b2023]
eos_strings = ['vdW EOS', 'Ronchi EOS', 'Beeler 2020', 'Beeler 2023']
for n, eos in zip(num_densities, eos_strings):
    print(f'{eos}:\t', [round(float(i / 1e30), 5) for i in n])

### Plotting
plt.figure(figsize=(5, 4))

plt.plot(Rb * 1e9, n_vdw,
         marker='v', ls=':',
         label=r'van der Waals (Y-L, $\gamma = 1.55$)')
plt.plot(Rb * 1e9, n_ronchi,
         marker='s', ls='-.',
         label=r'Ronchi (Y-L, $\gamma = 1.55$)')
plt.plot(Rb * 1e9, n_b2020,
         marker='o', ls='-.',
         label=r'Beeler 2020 (mod. Y-L, $\gamma = 1.2$)')
plt.plot(Rb * 1e9, n_b2023,
         marker='^', ls='--',
         label=r'Beeler 2023 (Y-L, $\gamma = 1.55$)')
plt.plot(r_md, n_md,
         marker='o', ls='-',
         label='MD simulations (ADP 2023)')

plt.xlabel(r'Bubble radius, $R_b$ (nm)')
# plt.ylabel(r'Molar volume, $v$ (cm$^3$/mol)')
# plt.ylabel(r'Xe/vac ratio, $\phi$')
plt.ylabel(r'Number density, $n$ (m$^{-3}$)')

plt.xscale('log')
# plt.yscale('log')

plt.legend()
plt.tight_layout()
plt.savefig('n_vs_rad.pdf')
