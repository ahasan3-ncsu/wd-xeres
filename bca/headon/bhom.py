import matplotlib.pyplot as plt

rad = [8, 16, 32, 64, 128]
bY = [5.8e-25, 1.8e-25, 5.9e-26, 2.3e-26, 1.2e-26]
bI = [7.5e-25, 2.4e-25, 8.0e-26, 3.4e-26, 1.8e-26]
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

plt.xlim([0, 140])
plt.ylim([1e-27, 1e-23])

plt.legend()
plt.tight_layout()
plt.savefig('bhom.pdf')
