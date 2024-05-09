#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt

files = sys.argv[1:]

plt.figure(figsize=(5,4))

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

    energy = file[file.find('ang')+3:file.find('pnm')] + '/nm'
    plt.plot(l_time[:len(j)], j, label=energy)
    plt.vlines(x=450, ymin=0, ymax=105, ls='dotted', colors='black')
    #plt.vlines(x=450, ymin=0, ymax=225, ls='dotted', colors='black')

plt.xlabel('Time (ps)')
plt.ylabel('Number of re-solved Xe atoms')
#plt.xlim(100, 1000)

plt.legend()
plt.tight_layout()
plt.savefig('resol_time.pdf')
