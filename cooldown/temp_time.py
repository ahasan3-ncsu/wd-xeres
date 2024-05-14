#!/usr/bin/env python

import sys
import itertools
import matplotlib.pyplot as plt

#fig = plt.figure(figsize=(5, 4), facecolor='lightblue')
fig = plt.figure(figsize=(5, 4))
ax = fig.add_axes([0.15, 0.15, 0.8, 0.8])

lines = itertools.cycle((
    'solid', 'dotted', 'dashed', 'dashdot', (0, (1, 1)), (0, (5, 1))
))

files = sys.argv[1:]

for file in files:
    with open(file) as f:
        l = f.readlines()

    l = l[2:]
    l_time = []
    l_temp = []
    l_resol = []
    for line in l:
        tmp = line.split()
        l_time.append(float(tmp[2]))
        l_temp.append(float(tmp[3]))
        l_resol.append(round(float(tmp[-1])))

    energy = file[file.find('ang')+3:file.find('keV')] + ' keV/nm'
    plt.plot(l_time, l_temp, ls=next(lines), label=energy)
    plt.vlines(x=450, ymin=500, ymax=2250, ls='dotted', colors='black')
    #plt.hlines(y=800, xmin=100, xmax=550, ls='dotted', colors='black')

plt.xlabel('Time (ps)')
plt.ylabel('Temperature (K)')
plt.xlim(80, 700)

plt.legend()
plt.savefig('temp_time.pdf')
