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
    for line in l:
        tmp = line.split()
        l_time.append(float(tmp[2]))

    frameFile = 'frames' + file[file.find('.'):]
    with open(frameFile) as f:
        j = f.readlines()
    j = [int(x) for x in j]

    energy = file[file.find('ang')+3:file.find('keV')] + ' keV/nm'
    plt.plot(l_time[:len(j)], j, ls=next(lines), label=energy)
    plt.vlines(x=450, ymin=0, ymax=105, ls='dotted', colors='black')
    #plt.vlines(x=450, ymin=0, ymax=225, ls='dotted', colors='black')

plt.xlabel('Time (ps)')
plt.ylabel('Number of re-solved Xe atoms')
plt.xlim(80, 700)

plt.legend()
plt.savefig('resol_time.pdf')
