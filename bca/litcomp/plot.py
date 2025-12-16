import numpy as np
import matplotlib.pyplot as plt

rad_this = [1, 2, 4, 8, 16, 32, 64, 128]
bhom_this = [
    8.70e-25, 4.74e-25, 2.67e-25, 1.60e-25,
    1.05e-25, 6.62e-26, 5.16e-26, 4.38e-26
]

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

plt.figure(figsize=(5, 4))

plt.plot(rad_this, bhom_this,
         marker='o', ls='-',
         label='U-10Mo (This work)')
plt.plot(rad_this, b_dart,
         marker='p', ls='-.',
         label='U-10Mo (DART)')
plt.plot(rad_uo2, bhet_uo2,
         marker='s', ls='--',
         label=r'UO$_2$ (Setyawan et al.)')
plt.plot(rad_uc, bhom_uc,
         marker='p', ls=':',
         label=r'UC (Matthews et al.)')

plt.xlabel(r'Bubble radius, $R_b$ (nm)')
plt.ylabel(r'$b$ / $\dot{F}$ (m$^3$/fsn)')

plt.xscale('log')
plt.yscale('log')

# plt.xlim([0, 140])
plt.ylim([1e-27, 1e-23])

plt.legend()
plt.tight_layout()
plt.savefig('comp.pdf')
