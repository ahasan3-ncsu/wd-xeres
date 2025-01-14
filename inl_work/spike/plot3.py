import numpy as np
import matplotlib.pyplot as plt
from statistics import mean, stdev
from scipy.optimize import curve_fit

def chi(x, alpha, cutoff):
    return 1 - np.exp(- alpha * (x - cutoff))

energ = [0.75, 3, 10, 15, 20, 25, 30, 35, 40]
energ = [x * 1e3 / 27.44 for x in energ]

xe_res = [[7, 6, 6], [25, 19, 19], [46, 33, 58], [65, 52, 59], [62, 75, 77], \
          [92, 107, 83], [132, 89, 86], [99, 107, 100], [101, 122, 94]]

xe_mean = [mean(x)/200 for x in xe_res]
xe_stdev = [stdev(x)/200 for x in xe_res]

plt.errorbar(energ, xe_mean, xe_stdev, capsize=3, marker='o',
             ls = 'none', label='200 atoms')

energ2 = [0.75, 3, 10, 15, 20, 25, 30, 35, 40]
energ2 = [x * 1e3 / 27.44 for x in energ2]

xe_res2 = [[9, 3, 3], [10, 25, 32], [90, 74, 63], [105, 116, 144], \
           [135, 163, 146], [188, 129, 140], [178, 182, 168], [182, 249, 229], \
           [190, 209, 224]]

xe_mean2 = [mean(x)/400 for x in xe_res2]
xe_stdev2 = [stdev(x)/400 for x in xe_res2]

plt.errorbar(energ2, xe_mean2, xe_stdev2, capsize=3, marker='o',
             ls = 'none', label='400 atoms')

xe_mean3 = [mean([x, y]) for x, y in zip(xe_mean, xe_mean2)]
p, c = curve_fit(chi, energ, xe_mean3, bounds=((0, 0), (1, 10)))
with open('param.txt', 'w') as f:
    f.write(f'{p}\n')

fit = [chi(x, *p) for x in energ]
plt.plot(energ, fit, c='k', label='fitted curve')

plt.xlabel('Energy deposited to the lattice (keV/nm)')
plt.ylabel('Fraction of resolved Xe atoms')
plt.legend()
plt.show()
