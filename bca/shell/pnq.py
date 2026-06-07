import itertools
import matplotlib.pyplot as plt

plt.style.use('../science.mplstyle')

def main():
    n = [0.8, 1.0, 1.2, 1.4]
    tot = [5375819, 6889284, 9251167, 11671554]
    out = [149491, 149869, 163857, 167961]
    res = [3681, 3629, 3880, 3934]

    tot_norm = [x/tot[1] for x in tot]
    out_norm = [x/out[1] for x in out]
    res_norm = [x/res[1] for x in res]

    markers = itertools.cycle(('o','x','^','v','s','p','+'))
    tints = itertools.cycle((0.2,0.8,1.0,0.6,0.4,0.0))
    lstyles = itertools.cycle(('-', '--', '-.', ':', (0, (5, 10))))

    plt.plot(
        n, tot_norm,
        marker=next(markers),
        color=plt.cm.jet(next(tints)),
        ls=next(lstyles),
        label='Total Xe recoils'
    )

    plt.plot(
        n, out_norm,
        marker=next(markers),
        color=plt.cm.jet(next(tints)),
        ls=next(lstyles),
        label='Xe outside bubble'
    )

    plt.plot(
        n, res_norm,
        marker=next(markers),
        color=plt.cm.jet(next(tints)),
        ls=next(lstyles),
        label='Re-solved Xe'
    )

    plt.xlabel(r'Relative Xe number density, $n$ / $n_{eq}$')
    plt.ylabel('Normalized quantity')

    plt.legend()
    plt.savefig('q_norm.pdf')

if __name__ == '__main__':
    main()
