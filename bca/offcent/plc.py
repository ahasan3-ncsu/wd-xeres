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

        m = chi[2]

        Rb = int(jname.split('_')[0][:-2]) * 10

        mark = next(markers)
        tint = next(tints)
        lsty = next(lstyles)

        if mode == 1:
            L = [l / Rb for l in L]

            # anchor right end to chi(E, R_b)
            # xa = np.linspace(0, 1, 100)
            # ya = [1 + (m-1) * x for x in xa]
            # plt.plot(
            #     xa, ya,
            #     color=plt.cm.jet(tint),
            #     ls=lsty
            # )
        elif mode == 2:
            L = [l - Rb for l in L]

            # anchor left end to chi(E, R_b)
            # xb = np.linspace(0, 1000, 100)
            # yb = [m * np.exp(-x/200) for x in xb]
            # plt.plot(
            #     xb, yb,
            #     color=plt.cm.jet(tint),
            #     ls=lsty
            # )

        plt.plot(
            L, chi,
            marker=mark,
            color=plt.cm.jet(tint),
            ls=lsty,
            label=f'{jname[:-5]}'
        )

        # plt.scatter(
        #     L, chi,
        #     marker=mark,
        #     color=plt.cm.jet(tint),
        # )
        #
        # plt.plot(
        #     [], [],
        #     marker=mark,
        #     color=plt.cm.jet(tint),
        #     ls=lsty,
        #     label=f'{jname[:-5]}'
        # )

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
