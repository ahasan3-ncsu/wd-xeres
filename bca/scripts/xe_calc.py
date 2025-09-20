#!/usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt

def calc(fileName, toPlot):
    E = []
    R_ini = []
    R_fin = []

    with open(fileName, 'r') as f:
        for line in f:
            if line[:6] == '134,54':
                tmp = line.split(',')
                E.append(float(tmp[2]))
                r2 = float(tmp[3])**2 + float(tmp[4])**2 + float(tmp[5])**2
                R_ini.append(r2**0.5)
                r2 = float(tmp[6])**2 + float(tmp[7])**2 + float(tmp[8])**2
                R_fin.append(r2**0.5)

    sorted_tuple = sorted(zip(E, R_ini, R_fin))
    E_sorted, R_ini_sorted, R_fin_sorted = zip(*sorted_tuple)

    print(
        ' Total Xe recoils: ', len(R_fin_sorted), '\n',
        'Outside the sphere: ', sum(1 for x in R_fin_sorted if x > 40), '\n',
        'Re-solved Xe: ', sum(1 for x in R_fin_sorted if x > 50)
    )

    if int(toPlot):
        up = []
        down = []

        for e, i, f in zip(E_sorted, R_ini_sorted, R_fin_sorted):
            if f > i:
                up.append([e, i])
            else:
                down.append([e, i])

        np_up = np.array(up)
        np_down = np.array(down)

        # scatters
        plt.scatter(np_up[:, 0], np_up[:, 1],
                    marker='^', s=5, color='orangered', label=r'$\mathbf{r_{i, ini}}$')
        plt.scatter(np_down[:, 0], np_down[:, 1],
                    marker='v', s=5, color='orangered')
        plt.scatter(E_sorted, R_fin_sorted,
                    marker='s', s=5, color='seagreen', label=r'$\mathbf{r_{i, fin}}$')

        # horizontal lines
        plt.hlines(40, xmin=1, xmax=1000,
                color='k', label=r'$R_b$')
        plt.hlines(50, xmin=1, xmax=1000,
                color='crimson', ls='--', label=r'$R_b + \delta$')

        plt.xscale('log')
        plt.yscale('log')

        plt.xlabel('Xe recoil energy (eV)')
        plt.ylabel(r'Distance from the bubble center ($\AA$)')

        plt.legend(loc='lower right')
        plt.savefig('/'.join(fileName.split('/')[:-1]) + '/xe_dist.pdf')

def main():
    args = sys.argv[1:]
    file = args[0]
    to_plot = args[1]

    calc(file, to_plot)

if __name__ == '__main__':
    main()
