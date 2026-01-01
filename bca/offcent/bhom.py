import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

rad = [1, 2, 4, 8, 16, 32, 64, 128]

# R_b/2 resolution up to 2 * R_b
# mean
bY = [
    3.33e-25, 1.87e-25, 9.51e-26, 6.01e-26,
    3.82e-26, 2.50e-26, 1.93e-26, 1.66e-26
]
bI = [
    5.37e-25, 2.87e-25, 1.72e-25, 1.00e-25,
    6.66e-26, 4.12e-26, 3.23e-26, 2.72e-26
]
b_mean = [y + i for y, i in zip(bY, bI)]
# print(b_mean)

# lower
bY = [
    1.70e-26, 1.78e-26, 2.05e-26, 2.28e-26,
    1.97e-26, 1.60e-26, 1.30e-26, 1.21e-26
]
bI = [
    7.27e-26, 6.42e-26, 4.65e-26, 4.19e-26,
    3.60e-26, 2.52e-26, 2.35e-26, 2.12e-26
]
b_lower = [y + i for y, i in zip(bY, bI)]

# upper
bY = [
    1.33e-24, 6.36e-25, 2.27e-25, 1.15e-25,
    6.42e-26, 3.58e-26, 2.65e-26, 2.14e-26
]
bI = [
    1.81e-24, 8.09e-25, 3.80e-25, 2.00e-25,
    1.07e-25, 5.95e-26, 4.17e-26, 3.35e-26
]
b_upper = [y + i for y, i in zip(bY, bI)]

# prep for errorbar
lo_err = [m - l for m, l in zip(b_mean, b_lower)]
up_err = [u - m for u, m in zip(b_upper, b_mean)]
# print(lo_err)
# print(up_err)

# do curve fitting here
def pl_fn(x, a, k, c):
    return a * x**k + c

b_scaled = [x * 1e26 for x in b_mean]
popt, pcov = curve_fit(
    pl_fn, rad, b_scaled,
    bounds=([0, -np.inf, 0], [np.inf, 0, np.inf])
)
# print(popt)

plt.figure(figsize=(5, 4))

plt.errorbar(
    rad, b_mean,
    [lo_err, up_err], capsize=3,
    marker='o', ls='', c=plt.cm.jet(0.2)
)

plt.plot(
    rad, pl_fn(rad, *popt) * 1e-26,
    ls='-', c=plt.cm.jet(0.8), label=r'$ax^k + c$'
)

plt.xlabel(r'Bubble radius, $R_b$ (nm)')
plt.ylabel(r'$b$ / $\dot{F}$ (m$^3$/fsn)')

plt.xscale('log')
plt.yscale('log')

# plt.xlim([0, 140])
plt.ylim([1e-26, 1e-23])

plt.legend()
plt.tight_layout()
plt.savefig('bhom.pdf')
