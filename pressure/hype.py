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

with open(files[0], 'r') as f:
    data = f.readlines()

k = [0,  1,  2,  3,  4,  5]
E = [5, 10, 15, 20, 25, 30]
xevac = [0.1, 0.2, 0.3, 0.5]

for ki, Ei in zip(k, E):
    start = 2+5*ki
    jar = data[start:start+5]

    res_1 = []; res_2 = []
    res_3 = []; res_5 = []
    for line in jar:
        tmp = line.split()
        res_1.append(int(tmp[0]))
        res_2.append(int(tmp[1]))
        res_3.append(int(tmp[2]))
        res_5.append(int(tmp[3]))

    print(res_1, res_2)
    print(res_3, res_5)

    res = [mean(res_1), mean(res_2), mean(res_3), mean(res_5)]
    dev = [stdev(res_1), stdev(res_2), stdev(res_3), stdev(res_5)]

    tag = f'{Ei}' + ' keV/nm'
    plt.errorbar(xevac, res, dev,
                 elinewidth=next(elines), capsize=5, capthick=next(thicks),
                 color=plt.cm.jet(next(tints)), marker=next(markers),
                 ls=next(lines), label=tag)

plt.xlabel(r'Xe/vac ratio of 25 $\AA$ radius bubble')
plt.ylabel('Number of re-solved Xe atoms')
plt.legend(loc='upper right', bbox_to_anchor=(0.90, 0.99))
plt.tight_layout()
plt.savefig('xevac.pdf')
