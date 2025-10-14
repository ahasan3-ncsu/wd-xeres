import sys
import matplotlib.pyplot as plt
import seaborn as sns
from toml_util import get_sphere_prop

def calc(disp_file, toml_file):
    R_ini = []
    R_fin = []

    with open(disp_file, 'r') as f:
        for line in f:
            if line[:6] == '134,54':
                tmp = line.split(',')

                r2 = float(tmp[3])**2 + float(tmp[4])**2 + float(tmp[5])**2
                R_ini.append(r2**0.5)
                r2 = float(tmp[6])**2 + float(tmp[7])**2 + float(tmp[8])**2
                R_fin.append(r2**0.5)

    Rb = get_sphere_prop(toml_file)
    L = 10

    print(
        ' Total Xe recoils: ', len(R_fin), '\n',
        'Outside the sphere: ', sum(1 for x in R_fin if x > Rb), '\n',
        'Re-solved Xe: ', sum(1 for x in R_fin if x > (Rb + L))
    )

    plt.figure(figsize=(5, 4))

    sns.histplot(
        R_ini, stat='frequency', binwidth=0.5,
        alpha=0.9, color='orangered', label=r'$\mathbf{r_{i, ini}}$'
    )
    sns.histplot(
        R_fin, stat='frequency', binwidth=0.5,
        alpha=0.7, color='seagreen', label=r'$\mathbf{r_{i, fin}}$'
    )

    plt.vlines(Rb, ymin=0, ymax=5050,
            color='k', lw=1, label=r'$R_b$')
    plt.vlines(Rb + L, ymin=0, ymax=5050,
            color='crimson', ls='--', lw=1, label=r'$R_b + \lambda$')

    plt.yscale('log')

    plt.xlim([max(0, Rb - 40), Rb + 60])

    plt.xlabel(r'Distance from bubble center ($\AA$)')
    plt.ylabel('Frequency')

    plt.legend()
    plt.tight_layout()
    plt.savefig('/'.join(disp_file.split('/')[:-1] + ['xe_hist.pdf']))

def main():
    file_root = sys.argv[1]
    disp_file = file_root + '_displacements.output'
    toml_file = file_root + '.toml'

    calc(disp_file, toml_file)

if __name__ == '__main__':
    main()
