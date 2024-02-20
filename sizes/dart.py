import numpy as np
import matplotlib.pyplot as plt

def bdart(r):
    if r <= 50:
        G = 1
    else:
        G = 1 - ((r-0.03)/r)**3
    return 2e-18 * G * 1e14

xs = np.linspace(1, 101, 25)
ys = [bdart(x) for x in xs]
plt.plot(xs, ys, color=plt.cm.jet(0.25), marker='o', label='DART')

plt.xlabel(r'Bubble radius, $R_{bubble}$ ($\AA$)')
plt.ylabel(r'Re-solution rate, $b_{het}$ ($s^{-1}$)')
plt.legend()
plt.ylim([1e-7, 1e-3])
plt.yscale('log')
plt.tight_layout()
plt.savefig('onlyDart.pdf')
