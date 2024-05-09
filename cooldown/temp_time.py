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
    l_temp = []
    l_resol = []
    for line in l:
        tmp = line.split()
        l_time.append(float(tmp[2]))
        l_temp.append(float(tmp[3]))
        l_resol.append(round(float(tmp[-1])))

    energy = file[file.find('ang')+3:file.find('pnm')] + '/nm'
    plt.plot(l_time, l_temp, label=energy)
    plt.vlines(x=450, ymin=500, ymax=2250, ls='dotted', colors='black')
    #plt.hlines(y=800, xmin=100, xmax=550, ls='dotted', colors='black')

plt.xlabel('Time (ps)')
plt.ylabel('Temperature (K)')
#plt.xlim(100, 1000)

plt.legend()
plt.tight_layout()
plt.savefig('temp_time.pdf')
