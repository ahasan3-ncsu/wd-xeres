import os
import json
import itertools
import matplotlib.pyplot as plt

def plotter(jpath):
    markers = itertools.cycle(('o','s','p','v','x','+','^'))
    tints = itertools.cycle((0.2,0.8,0.4,0.6,0.0,1.0))
    lstyles = itertools.cycle(('-', '--', ':', '-.', (0, (5, 10))))

    plt.figure(figsize=(5, 4))

    with open(jpath, 'r') as f:
        foo = json.load(f)

    L = foo['L']
    E = foo['E']
    chi = foo['chi']

    for i, l in enumerate(L):
        mark = next(markers)
        tint = next(tints)
        lsty = next(lstyles)

        plt.plot(
            E, chi[i],
            marker=mark,
            color=plt.cm.jet(tint),
            ls=lsty,
            label=rf'$\ell$ = {l/10:.0f} nm'
        )

    plt.title(f'{jpath.split('/')[-1][:-5]}')
    plt.xlabel('Energy (MeV)')
    plt.ylabel(r'Re-solved bubble fraction, $\chi(E, \ell)$')

    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    data_dir = 'data'
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    print(json_files)

    for jname in json_files:
        jpath = os.path.join(data_dir, jname)
        plotter(jpath)

if __name__ == '__main__':
    main()
