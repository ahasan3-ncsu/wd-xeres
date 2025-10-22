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
    lines = itertools.cycle(('-', '--', ':', '-.', (0, (5, 10))))

    for jname in json_files:
        jpath = os.path.join(data_dir, jname)
        with open(jpath, 'r') as f:
            foo = json.load(f)

        L = foo['L']
        chi = foo['chi']

        # to normalize by bubble radius
        Rb = int(jname.split('_')[0][:-2]) * 10

        # normalize
        # L = [l / L[-1] for l in L]
        L = [l / Rb for l in L]
        chi = [c / chi[0] for c in chi]

        plt.plot(
            L, chi,
            marker=next(markers),
            color=plt.cm.jet(next(tints)),
            ls=next(lines),
            label=f'{jname[:-5]}'
        )

    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
