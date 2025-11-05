import matplotlib.pyplot as plt

rad = [1, 2, 4, 8, 16, 32, 64, 128]

# constant mesh element size
oldY = [
    6.29e-24, 1.64e-24, 4.67e-25, 1.28e-25,
    4.39e-26, 2.59e-26, 1.63e-26, 1.53e-26
]
oldI = [
    6.92e-24, 2.22e-24, 6.22e-25, 1.91e-25,
    7.13e-26, 4.10e-26, 2.67e-26, 2.46e-26
]
oldB = [y + i for y, i in zip(oldY, oldI)]

# R_b/2 resolution up to 4 * R_b
bY = [
    3.36e-25, 1.99e-25, 9.89e-26, 5.84e-26,
    3.54e-26, 2.48e-26, 1.83e-26, 1.63e-26
]
bI = [
    5.66e-25, 2.93e-25, 1.77e-25, 9.97e-26,
    6.19e-26, 4.09e-26, 3.08e-26, 2.65e-26
]
bhom = [y + i for y, i in zip(bY, bI)]

def bdart(r):
    b0 = 2e-24 # m^3
    if r <= 5: # nm
        G = 1
    else:
        G = 1 - ((r - 3e-2) / r)**3
    return b0 * G

dart = [bdart(r) for r in rad]

plt.figure(figsize=(5, 4))

plt.plot(rad, oldB, marker='v', ls=':', label='Constant mesh')
plt.plot(rad, bhom, marker='o', ls='-', label='Variable mesh')
plt.plot(rad, dart, marker='^', ls='--', label='DART')

plt.xlabel(r'Bubble radius, $R_b$ (nm)')
plt.ylabel(r'$b$ / $\dot{F}$ (m$^3$/fsn)')

plt.xscale('log')
plt.yscale('log')

# plt.xlim([0, 140])
# plt.ylim([1e-27, 1e-23])

plt.legend()
plt.tight_layout()
plt.savefig('bhom.pdf')
