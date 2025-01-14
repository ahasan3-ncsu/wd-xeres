import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def func(x, a, b, c, d, e, f):
    return a * np.exp(-b * x**c) + d * np.exp(-e * x**f)

with open('store.txt', 'r') as f:
    jar = f.readlines()

energ = []; Se = []
for line in jar:
    tmp = line.split()
    energ.append(float(tmp[0]))
    Se.append(float(tmp[1]) / 1e2)

#plt.plot(energ, Se)
#plt.show()

L = len(energ)

dst = []
cur = 0
for i in range(L-1, 0, -1):
    cur += (energ[i] - energ[i-1]) / Se[i] / 1e6
    dst.append(cur)

dst.reverse()
plt.scatter(dst, Se[1:], label='SRIM data')

param, coeff = curve_fit(func, dst, Se[1:], bounds=((0), (50)))
fit = [func(x, *param) for x in dst]

with open('params.txt', 'w') as f:
    f.write(f'{param}\n')

plt.plot(dst, fit, c='k', label='fitted curve')

plt.xlabel(r'Distance ($\mu m$)')
plt.ylabel(r'$S_e$ (keV/nm)')
plt.legend()
plt.show()
