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
    lstyles = itertools.cycle(('-', '--', ':', '-.', (0, (5, 10))))

    plt.figure(figsize=(5,4))

    for jname in json_files:
        jpath = os.path.join(data_dir, jname)
        with open(jpath, 'r') as f:
            foo = json.load(f)

        L = foo['L']
        chi = foo['chi']

        chi = [c / chi[0] for c in chi]

        Rb = int(jname.split('_')[0][:-2]) * 10

        if mode == 1:
            L = [l / Rb for l in L]
        elif mode == 2:
            L = [l - Rb for l in L]
        elif mode == 3:
            L = [l / L[-1] for l in L]

        mark = next(markers)
        tint = next(tints)
        lsty = next(lstyles)

        # plt.plot(
        #     L, chi,
        #     marker=mark,
        #     color=plt.cm.jet(tint),
        #     ls=lsty,
        #     label=f'{jname[:-5]}'
        # )

        def fit(x, x1, y1, x2, y2):
            if x < x1:
                return 1 + (y1 - 1) / x1 * x
            else:
                c = (x2 - x1) / np.log(y1 / y2)
                return y1 * np.exp(-(x - x1) / c)
        xc = np.linspace(0, L[-1], 100)
        yc = [
            fit(x, L[4], chi[4], L[-4], chi[-4])
            for x in xc
        ]

        plt.plot(
            xc, yc,
            color=plt.cm.jet(tint),
            ls=lsty
        )

        plt.scatter(
            L, chi,
            marker=mark,
            color=plt.cm.jet(tint),
        )

        plt.plot(
            [], [],
            marker=mark,
            color=plt.cm.jet(tint),
            ls=lsty,
            label=f'{jname[:-5]}'
        )

    if mode == 1:
        plt.xlim([0, 1])
        plt.xlabel(r'$\ell$ / $R_b$')
    elif mode == 2:
        plt.xlim([0, 1000])
        plt.xlabel(r'$\ell$ - $R_b$')
    elif mode == 3:
        plt.xlabel(r'$\ell$ / ($R_b + \delta$)')
    elif mode == 4:
        plt.xlabel(r'$\ell$')

    plt.ylabel(r'$\chi(E, \ell)$ / $\chi(E, 0)$')

    plt.legend()
    plt.tight_layout()
    plt.savefig(f'offcent_{mode}.pdf')

def main():
    data_dir = 'data'

    plotter(data_dir, 1)
    plotter(data_dir, 2)
    plotter(data_dir, 3)
    plotter(data_dir, 4)

if __name__ == '__main__':
    main()
