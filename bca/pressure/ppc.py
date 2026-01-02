import os
import json
import itertools
import matplotlib.pyplot as plt

plt.style.use('../science.mplstyle')

def main():
    data_dir = 'data'
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    json_files.sort()
    json_files = json_files[4:] + json_files[:4]
    print(json_files)

    markers = itertools.cycle(('o','x','^','v','s','p','+'))
    tints = itertools.cycle((0.2,0.8,0.4,0.6,0.0,1.0))
    lstyles = itertools.cycle(('-', '--', ':', '-.', (0, (5, 10))))

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
            marker=mark, s=25,
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
    plt.ylim([2e-10, 2e-5])

    plt.xlabel(r'Relative Xe number density, $n$ / $n_{eq}$')
    plt.ylabel(r'Re-solved bubble fraction, $\chi(E, 0)$')

    plt.legend(fontsize=8, ncol=2, loc='lower left')
    plt.savefig('pressure.pdf')
    plt.close()

if __name__ == '__main__':
    main()
