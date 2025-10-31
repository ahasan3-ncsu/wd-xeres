import matplotlib.pyplot as plt

rad = [1, 2, 4, 8, 16, 32, 64, 128]
bY = [
    6.29e-24, 1.64e-24, 4.67e-25, 1.28e-25,
    4.39e-26, 2.59e-26, 1.63e-26, 1.53e-26
]
bI = [
    6.92e-24, 2.22e-24, 6.22e-25, 1.91e-25,
    7.13e-26, 4.10e-26, 2.67e-26, 2.46e-26
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

plt.plot(rad, bhom, marker='o', ls='-', label='This work')
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
