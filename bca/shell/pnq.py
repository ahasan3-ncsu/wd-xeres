import itertools
import matplotlib.pyplot as plt

plt.style.use('../science.mplstyle')

def normalize(lst):
    return [x / lst[1] for x in lst]

def main():
    n = [0.8, 1.0, 1.2, 1.4]
    tot = [5375819, 6889284, 9251167, 11671554]
    mfp = [1.194, 0.952, 0.788, 0.670]
    out = [149491, 149869, 163857, 167961]
    res = [3681, 3629, 3880, 3934]

    markers = itertools.cycle(('o','x','^','p','v','s','+'))
    tints = itertools.cycle((0.2,0.8,1.0,0.4,0.6,0.0))
    lstyles = itertools.cycle(('-', '--', '-.', ':', (0, (5, 10))))

    plots = [
        (normalize(tot), 'Total Xe recoils'),
        (normalize(mfp), 'Mean free path'),
        (normalize(out), 'Xe outside bubble'),
        (normalize(res), 'Re-solved Xe'),
    ]

    for y, lbl in plots:
        plt.plot(
            n, y,
            marker=next(markers),
            color=plt.cm.jet(next(tints)),
            ls=next(lstyles),
            label=lbl
        )

    plt.xlabel(r'Relative Xe number density, $n$ / $n_{eq}$')
    plt.ylabel('Normalized quantity')

    plt.legend()
    plt.savefig('q_norm.pdf')

if __name__ == '__main__':
    main()
