import numpy as np
import matplotlib.pyplot as plt

rad_this = [1, 2, 4, 8, 16, 32, 64, 128]
bhom_this = [
    8.77e-25, 4.81e-25, 2.62e-25, 1.60e-25,
    1.04e-25, 6.62e-26, 5.16e-26, 4.38e-26
]
lo_err = [
    7.87e-25, 3.99e-25, 1.95e-25, 9.55e-26,
    4.83e-26, 2.50e-26, 1.51e-26, 1.05e-26
]
up_err = [
    2.26e-24, 9.64e-25, 3.45e-25, 1.55e-25,
    6.72e-26, 2.91e-26, 1.66e-26, 1.11e-26
]

def pl_fn(x):
    return 8.43e-25 * x**(-0.926) + 3.46e-26

pl_fit = [pl_fn(x) for x in rad_this]

def bdart(r):
    b0 = 2e-24 # m^3
    if r <= 5: # nm
        G = 1
    else:
        G = 1 - ((r - 3e-2) / r)**3
    return b0 * G

b_dart = [bdart(r) for r in rad_this]

rad_uo2 = [0.6, 0.8, 1.5, 2, 3]
bhet_uo2 = [
    0.949 * np.exp(-0.0703 * x) * 1e-25
    + (9.1816 - 0.949) / (1 + 7.982 * x**2)
        * np.exp(-0.0371 * x**2) * 1e-25
    for x in rad_uo2
]

rad_uc = [
    0.511, 0.815, 1.191, 1.689, 2.397, 3.401, 4.968,
    10.91, 23.28, 48.25, 48.25, 106.0, 201.2
]
bhom_uc = [
    x * 1e-25 for x in
    [2.364, 2.168, 2.000, 1.844, 1.689, 1.540, 1.385,
    1.114, 0.959, 0.885, 0.885, 0.837, 0.817]
]

rad_uzr = list(range(100, 1001, 100))

plt.style.use('../science.mplstyle')
plt.figure(figsize=(3.5, 3.5))

plt.plot(rad_uo2, bhet_uo2,
         marker='s', ls='--', c=plt.cm.jet(0.4),
         label=r'UO$_2$ (Setyawan et al.)')
plt.plot(rad_uc, bhom_uc,
         marker='v', ls=':', c=plt.cm.jet(0.8),
         label=r'UC (Matthews et al.)')
plt.plot(rad_this, b_dart,
         marker='p', ls='-.', c=plt.cm.jet(0.6),
         label='U-10Mo (DART)')

plt.errorbar(rad_this, bhom_this,
         [lo_err, up_err], capsize=3,
         marker='o', ls='', c=plt.cm.jet(0.2),
         label='U-10Mo (This work)')
plt.plot(rad_this, pl_fit, ls='-', c=plt.cm.jet(0.2))

plt.xlabel(r'Bubble radius, $R_b$ (nm)')
plt.ylabel(r'$b$ / $\dot{F}$ (m$^3$/fsn)')

plt.xscale('log')
plt.yscale('log')

plt.ylim([1e-28, 1e-23])

plt.legend()
plt.savefig('comp.pdf')
