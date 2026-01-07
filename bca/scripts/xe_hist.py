import sys
import matplotlib.pyplot as plt
import seaborn as sns
from toml_util import get_sphere_prop

plt.style.use('../science.mplstyle')

def calc(disp_file, toml_file):
    R_ini = []
    R_fin = []

    with open(disp_file, 'r') as f:
        for line in f:
            if line[:6] == '134,54':
                tmp = line.split(',')

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

    sns.histplot(
        R_ini, stat='frequency', binwidth=0.1,
        color=plt.cm.jet(0.9), element='step',
        label=r'$\mathbf{r_{i, ini}}$'
    )
    sns.histplot(
        R_fin, stat='frequency', binwidth=0.1,
        alpha=0.5, color=plt.cm.jet(0.3), element='step',
        label=r'$\mathbf{r_{i, fin}}$'
    )

    plt.vlines(Rb, ymin=0, ymax=3e3,
            color='k', lw=1, label=r'$R_b$')
    plt.vlines(Rb + L, ymin=0, ymax=3e3,
            color='orange', ls='--', lw=1, label=r'$R_b + \lambda$')

    plt.yscale('log')

    plt.xlim([max(0, Rb - 4), Rb + 6])

    plt.xlabel('Distance from bubble center (nm)')
    plt.ylabel('Frequency')

    plt.legend()
    plt.savefig('/'.join(disp_file.split('/')[:-1] + ['xe_hist.pdf']))

def main():
    file_root = sys.argv[1]
    disp_file = file_root + '_displacements.output'
    toml_file = file_root + '.toml'

    calc(disp_file, toml_file)

if __name__ == '__main__':
    main()
