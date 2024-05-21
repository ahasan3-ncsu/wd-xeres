#!/usr/bin/env python

import sys
import itertools
import matplotlib.pyplot as plt
from statistics import mean, stdev

tints = itertools.cycle((0.0,0.2,0.4,0.6,0.8,1.0))
markers = itertools.cycle(('o','s','p','v','>','<'))
lines = itertools.cycle(('-', '--', ':', '-.',
                         (0, (5, 10)), (0, (3, 1, 1, 10))))
elines = itertools.cycle((1, 1.4, 1.8, 2.2, 2.6, 3))
#thicks = itertools.cycle((3, 2.6, 2.2, 1.8, 1.4, 1))
thicks = itertools.cycle((1, 1.4, 1.8, 2.2, 2.6, 3))

files = sys.argv[1:]

# hardcoded
with open(files[0], 'r') as f:
    data15 = f.readlines()

with open(files[1], 'r') as f:
    data25 = f.readlines()

with open(files[2], 'r') as f:
    data35 = f.readlines()

k = [0,  1,  2,  3,  4,  5]
E = [5, 10, 15, 20, 25, 30]
#xevac = [0.1, 0.2, 0.3, 0.5]
radii = [15, 25, 35]
rad2 = [i**2 for i in radii]

res_E = [[] for i in range(6)]
dev_E = [[] for i in range(6)]

for dat in [data15, data25, data35]:
    for ki, Ei in zip(k, E):
        start = 2+5*ki
        jar = dat[start:start+5]

        resall = []
        for line in jar:
            tmp = line.split()
            for ii in [0, 1, 2, 3]:
                resall.append(int(tmp[ii]))

        res_E[ki].append(mean(resall))
        dev_E[ki].append(stdev(resall))

print(res_E)
for res, dev, Ei in zip(res_E, dev_E, E):
    tag = f'{Ei}' + ' keV/nm'
    plt.errorbar(radii, res, dev,
                 elinewidth=next(elines), capsize=5, capthick=next(thicks),
                 color=plt.cm.jet(next(tints)), marker=next(markers),
                 ls=next(lines), label=tag)

plt.ylim([-5, 80])
plt.xlabel(r'Bubble radius, $R_{bubble}$ ($\AA$)')
plt.ylabel('Number of re-solved Xe atoms')
plt.legend(loc='upper right', bbox_to_anchor=(0.90, 0.99))
plt.tight_layout()
plt.savefig('r2dep.pdf')
