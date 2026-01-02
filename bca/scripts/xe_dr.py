import sys
import numpy as np
import matplotlib.pyplot as plt
from toml_util import get_sphere_prop

plt.style.use('../science.mplstyle')

def calc(disp_file, toml_file, save_ext):
    E = []
    E_max = 0
    E_min = 1e9
    R_ini = []
    R_fin = []

    with open(disp_file, 'r') as f:
        for line in f:
            if line[:6] == '134,54':
                tmp = line.split(',')

                energ = float(tmp[2])
                E.append(energ)
                if energ > E_max:
                    E_max = energ
                if energ < E_min:
                    E_min = energ

                r2 = float(tmp[3])**2 + float(tmp[4])**2 + float(tmp[5])**2
                R_ini.append(r2**0.5 / 10) # nm
                r2 = float(tmp[6])**2 + float(tmp[7])**2 + float(tmp[8])**2
                R_fin.append(r2**0.5 / 10) # nm

    Rb = get_sphere_prop(toml_file) / 10 # nm
    L = 1 # nm

    print(
        ' Total Xe recoils: ', len(R_fin), '\n',
        'Outside the sphere: ', sum(1 for x in R_fin if x > Rb), '\n',
        'Re-solved Xe: ', sum(1 for x in R_fin if x > (Rb + L))
    )

    up = []
    down = []

    for e, i, f in zip(E, R_ini, R_fin):
        if f > i:
            up.append([e, i])
        else:
            down.append([e, i])

    np_up = np.array(up)
    np_down = np.array(down)

    # scatters
    plt.scatter(np_up[:, 0], np_up[:, 1],
                marker='^', s=5, color=plt.cm.jet(0.9),
                label=r'$\mathbf{r_{i, ini}}$', rasterized=True)
    plt.scatter(np_down[:, 0], np_down[:, 1],
                marker='v', s=5, color=plt.cm.jet(0.9), rasterized=True)
    plt.scatter(E, R_fin, alpha=0.5,
                marker='s', s=3, color=plt.cm.jet(0.3),
                label=r'$\mathbf{r_{i, fin}}$', rasterized=True)

    # horizontal lines
    plt.hlines(Rb, xmin=0.9*E_min, xmax=1.1*E_max,
            color='k', lw=1, label=r'$R_b$')
    plt.hlines(Rb + L, xmin=0.9*E_min, xmax=1.1*E_max,
            color='orange', ls='--', lw=1, label=r'$R_b + \lambda$')

    plt.xscale('log')

    plt.ylim([max(0, Rb - 4), Rb + 6])

    plt.xlabel('Xe recoil energy (eV)')
    plt.ylabel('Distance from bubble center (nm)')

    plt.legend(ncols=2)
    plt.savefig(
        '/'.join(disp_file.split('/')[:-1] + [f'xe_dr.{save_ext}']),
        dpi=500
    )

def main():
    file_root = sys.argv[1]
    disp_file = file_root + '_displacements.output'
    toml_file = file_root + '.toml'
    save_ext = sys.argv[2]

    calc(disp_file, toml_file, save_ext)

if __name__ == '__main__':
    main()
