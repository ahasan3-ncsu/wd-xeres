import matplotlib.pyplot as plt

rad = [1, 2, 4, 8, 16, 32, 64, 128]
bY = [
    2.98e-23, 7.97e-24, 2.20e-24, 5.49e-25,
    1.43e-25, 4.18e-26, 1.53e-26, 8.33e-27
]
bI = [
    3.28e-23, 1.04e-23, 2.70e-24, 7.67e-25,
    2.09e-25, 5.86e-26, 2.34e-26, 1.36e-27
]
b = [y + i for y, i in zip(bY, bI)]

def bdart(r):
    b0 = 2e-24 # m^3
    if r <= 5: # nm
        G = 1
    else:
        G = 1 - ((r - 3e-2) / r)**3
    return b0 * G

mr = [1, 2, 4] + rad
bd = [bdart(r) for r in mr]

plt.figure(figsize=(5, 4))

plt.plot(rad, b, marker='o', ls='-', label='This work')
plt.plot(mr, bd, marker='^', ls='--', label='DART')

plt.xlabel(r'Bubble radius, $R_b$ (nm)')
plt.ylabel(r'$b$ / $\dot{F}$ (m$^3$/fsn)')

# plt.xscale('log')
plt.yscale('log')

# plt.xlim([0, 140])
# plt.ylim([1e-27, 1e-23])

plt.legend()
plt.tight_layout()
plt.savefig('bhom.pdf')
