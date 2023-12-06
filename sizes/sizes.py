import numpy as np
from statistics import mean, stdev
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

size_5 = [[0, 5, 4, 1, 4.2256], [5, 2, 4, 5, 3], [4, 4, 5, 5, 4],
        [4, 4, 4, 5, 4], [4, 4, 4.671, 5, 5], [5, 5, 5, 5, 5]]

size_10 = [[0.0664, 0, 0, 1, 0], [9, 11.0846, 6, 5.407, 11],
        [27.8656, 13.3168, 10.149, 16.6342, 36.7528],
        [38.8424, 36.9786, 35.7044, 14, 31.4588],
        [23, 25.0252, 24.2368, 39, 22.2026],
        [40, 30.2768, 30, 39.6754, 31.799]]

size_15 = [[0, 0, 1, 0, 1], [9.2706, 9, 10, 4, 6],
           [23.0902, 20, 23.4742, 15.7396, 10],
           [32.9472, 36.1752, 19, 73.7984, 21.8784],
           [33, 63, 37, 25.751, 86.6162], [40, 39.7268, 50.9582, 79.249, 42]]

size_20 = [[0, 1, 0, 0, 0], [4.0422, 14, 9, 17, 9], [23, 26, 23, 19, 25],
           [31, 22.651, 28, 37, 30.1736], [47, 40, 41, 29.7506, 41.0226],
           [32, 46, 113.707, 45.0224, 38]]

size_25 = [[1, 1, 0, 2, 0], [9, 123.807, 4, 3, 7.3474],
           [19.6004, 31.9774, 15, 16, 14.4424], [30.9592, 26, 60, 39.9322, 44],
           [41, 30, 56, 36, 39.68], [43.8896, 39.92, 43, 81.3994]]

size_30 = [[1, 1, 3, 0, 0], [5, 8, 12, 6, 9.9232], [11, 23, 21, 14, 17],
           [43, 33.3008, 41.8402, 47, 30], [47, 44.0182, 60, 67, 36.8966],
           [41, 69, 72, 49.5552, 42]]

size_35 = [[0, 2, 1.5492, 0, 0.496], [5, 15, 16, 8, 13.8516],
           [12, 26, 16, 28, 116.525], [27, 22, 29, 26, 41],
           [44, 32.2946, 45, 23, 40], [51.5568, 46.8746, 48.594, 108.708, 72]]

size_40 = [[1.6872, 6.2584, 6.1962, 5, 1.029], [13, 27.3302, 1, 11, 10],
           [16, 53.3704, 13, 22, 17], [13, 14, 20, 26, 23.7902],
           [25.8116, 26, 35, 30, 36], [25, 50, 46, 33, 35]]

radii = [5, 10, 15, 20, 25, 30, 35, 40]
energies = [5, 10, 15, 20, 25, 30]
xe_num = [5, 41, 138, 328, 641, 1107, 1758, 2624]

averages = []; std_devs = []
for i, sz in enumerate([size_5, size_10, size_15, size_20,
               size_25, size_30, size_35, size_40]):
    averages.append([mean(x)/xe_num[i] for x in sz])
    std_devs.append([stdev(x)/xe_num[i] for x in sz])

plt.figure(figsize=(7,4))
for r, y_data, e_data, mark in zip(radii, averages, std_devs,
                                   ['o','s','p','x','v','^', '>', '<']):
    plt.errorbar(energies, y_data, e_data, color=plt.cm.gist_rainbow(r/40),
                 marker=mark, ls='', capsize=3, label=f'{r} '+r'$\AA$')

def chi(x, alpha):
    return 1 - np.exp(-alpha * x)

alphs = []
for y_data in averages:
    p, c = curve_fit(chi, energies, y_data, bounds=(0, 1))
    alphs.append(*p)
print('alphas: ', alphs)

ens = np.linspace(0, 30, 100)
for a, r in zip(alphs, radii):
    plt.plot(ens, chi(ens, a), c=plt.cm.gist_rainbow(r/40))

plt.xlabel(r'Effective energy transferred to the lattice, $S_{e,eff}$ (keV/nm)')
plt.ylabel(r'Fraction of re-solved Xe, $\chi_0$')
plt.legend(handletextpad=0)
#plt.show()
plt.tight_layout()
plt.savefig('resolutionVsRadius.pdf')

def sat(x, a, b):
    return a / x**b

p, c = curve_fit(sat, radii, alphs, sigma=[5, 3, 2, 1, 1, 1, 1, 1])
print('saturating factor: ', *p)

xs = np.linspace(4, 44, num=100)
ys = sat(xs, *p)

plt.figure(figsize=(3,4))
plt.scatter(radii, alphs, color=plt.cm.jet(0.2), label=r'$\alpha$')
plt.plot(xs, ys, color=plt.cm.jet(0.8), label='Fit')

plt.xlabel(r'Bubble radius, $R_{bubble}$ ($\AA$)')
plt.ylabel(r'Saturation factor, $\alpha$ (nm/keV)')
plt.legend()
#plt.show()
plt.tight_layout()
plt.savefig('saturationFactor.pdf')
