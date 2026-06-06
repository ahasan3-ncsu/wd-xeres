import itertools
import matplotlib.pyplot as plt

plt.style.use('../science.mplstyle')

def main():
    n = [0.8, 1.0, 1.2, 1.4]
    pos = [54.278, 54.860, 55.108, 56.062]
    std = [11.539, 11.315, 11.592, 10.769]

    t = [64 - i for i in pos]
    print(t)

    pred1 = [9.14 / i for i in n]
    pred2 = [9.14 for _ in n]

    markers = itertools.cycle(('o','x','^','v','s','p','+'))
    tints = itertools.cycle((0.2,0.8,1.0,0.6,0.4,0.0))
    lstyles = itertools.cycle(('-', '--', '-.', ':', (0, (5, 10))))

    plt.errorbar(
        n, t,
        [2 * s for s in std],
        marker=next(markers),
        color=plt.cm.jet(next(tints)),
        ls=next(lstyles),
        capsize=3,
        label='Data'
    )

    plt.plot(
        n, pred1,
        marker=next(markers),
        color=plt.cm.jet(next(tints)),
        ls=next(lstyles),
        label='t = 1/n'
    )

    plt.plot(
        n, pred2,
        marker=next(markers),
        color=plt.cm.jet(next(tints)),
        ls=next(lstyles),
        label='t = const'
    )

    plt.xlabel(r'Relative Xe number density, $n$ / $n_{eq}$')
    plt.ylabel(
        'Avg. initial distance of re-solved Xe \n' +
        r'from the bubble surface, $t$ (nm)'
    )

    plt.legend()
    plt.savefig('shell.pdf')

if __name__ == '__main__':
    main()
