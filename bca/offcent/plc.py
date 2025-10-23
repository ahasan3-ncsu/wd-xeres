import os
import json
import itertools
import numpy as np
import matplotlib.pyplot as plt

def plotter(data_dir, mode=1):
    json_files = sorted([f for f in os.listdir(data_dir) if f.endswith('.json')])
    print(json_files)

    markers = itertools.cycle(('o','s','p','v','x','+','^'))
    tints = itertools.cycle((0.2,0.8,0.4,0.6,0.0,1.0))
    lines = itertools.cycle(('-', '--', ':', '-.', (0, (5, 10))))

    plt.figure(figsize=(5,4))

    for jname in json_files:
        jpath = os.path.join(data_dir, jname)
        with open(jpath, 'r') as f:
            foo = json.load(f)

        L = foo['L']
        chi = foo['chi']

        # normalize by R_b
        Rb = int(jname.split('_')[0][:-2]) * 10
        if mode == 1:
            L = [l / Rb for l in L]

            xa = np.linspace(0, 1, 100)
            ya = [1 for x in xa]
            plt.plot(xa, ya, color='k', ls='--')
        elif mode == 2:
            L = [l - Rb for l in L]

            xb = np.linspace(0, 1000, 100)
            yb = [np.exp(-x/200) for x in xb]
            plt.plot(xb, yb, color='k', ls='--')

        chi = [c / chi[0] for c in chi]

        plt.plot(
            L, chi,
            marker=next(markers),
            color=plt.cm.jet(next(tints)),
            ls=next(lines),
            label=f'{jname[:-5]}'
        )

    if mode == 1:
        plt.xlim([0, 1])
        plt.xlabel(r'$\ell$ / $R_b$')
    elif mode == 2:
        plt.xlim([0, 1000])
        plt.xlabel(r'$\ell$ - $R_b$')

    plt.ylabel(r'$\chi(E, \ell)$ / $\chi(E, 0)$')

    plt.legend()
    plt.tight_layout()
    plt.savefig(f'offcent_{mode}.pdf')

def main():
    data_dir = 'data'

    plotter(data_dir, 1)
    plotter(data_dir, 2)

if __name__ == '__main__':
    main()
