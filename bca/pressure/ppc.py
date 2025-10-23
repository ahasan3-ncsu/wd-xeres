import os
import json
import itertools
import matplotlib.pyplot as plt

def main():
    data_dir = 'data'
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    print(json_files)

    markers = itertools.cycle(('o','s','p','v','x','+','^'))
    tints = itertools.cycle((0.2,0.8,0.4,0.6,0.0,1.0))
    lstyles = itertools.cycle(('-', '--', ':', '-.', (0, (5, 10))))

    plt.figure(figsize=(5, 4))

    for jname in json_files:
        jpath = os.path.join(data_dir, jname)
        with open(jpath, 'r') as f:
            foo = json.load(f)

        P = foo['P']
        rxe = foo['rxe']
        chi = foo['chi']

        mark = next(markers)
        tint = next(tints)
        lsty = next(lstyles)

        # plt.plot(
        #     P, rxe,
        #     marker=next(markers),
        #     color=plt.cm.jet(next(tints)),
        #     ls=next(lines),
        #     label=f'{jname[:-5]}'
        # )
        # plt.hlines(rxe[1], 0.8, 1.4, color='k', ls=':')

        plt.scatter(
            P, chi,
            marker=mark,
            color=plt.cm.jet(tint)
        )

        pred = [chi[1] / x for x in P]
        plt.plot(
            P, pred,
            color=plt.cm.jet(tint),
            ls=lsty
        )

        plt.plot(
            [], [],
            marker=mark,
            color=plt.cm.jet(tint),
            ls=lsty,
            label=f'{jname[:-5]}'
        )

    plt.yscale('log')
    plt.ylim([2e-9, 2e-5])

    plt.xlabel(r'Relative Xe number density, $n$ / $n_{eq}$')
    plt.ylabel(r'Re-solved bubble fraction, $\chi(E, 0)$')

    plt.legend(ncol=2, bbox_to_anchor=[0.5, 0.15], loc='center')
    plt.tight_layout()
    plt.savefig('pressure.pdf')

if __name__ == '__main__':
    main()
