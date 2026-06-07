import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from statistics import mean, stdev
from toml_util import get_sphere_prop

plt.style.use('../science.mplstyle')

def calc(disp_file, toml_file, xe_file):
    R_ini = []
    R_fin = []

    if os.path.isfile(xe_file):
        print(f'Using {xe_file} file...')

        with open(xe_file, 'r') as f:
            for line in f:
                tmp = line.split(',')

                r2 = float(tmp[3])**2 + float(tmp[4])**2 + float(tmp[5])**2
                R_ini.append(r2**0.5 / 10) # nm
                r2 = float(tmp[6])**2 + float(tmp[7])**2 + float(tmp[8])**2
                R_fin.append(r2**0.5 / 10) # nm
    else:
        print(f'Using {disp_file} file...')

        xe_output = ''
        with open(disp_file, 'r') as f:
            for line in f:
                if line[:6] == '134,54':
                    xe_output += line

                    tmp = line.split(',')

                    r2 = float(tmp[3])**2 + float(tmp[4])**2 + float(tmp[5])**2
                    R_ini.append(r2**0.5 / 10) # nm
                    r2 = float(tmp[6])**2 + float(tmp[7])**2 + float(tmp[8])**2
                    R_fin.append(r2**0.5 / 10) # nm

        with open(xe_file, 'w') as f:
            f.write(xe_output)

    Rb = get_sphere_prop(toml_file) / 10 # nm
    L = 1 # nm

    Dist = [abs(y - x) for x, y in zip(R_ini, R_fin)]

    print(
        ' Total Xe recoils: ', len(R_fin), '\n',
        'Mean Xe displacement: ', mean(Dist), '\n',
        'Outside the sphere: ', sum(1 for x in R_fin if x > Rb), '\n',
        'Re-solved Xe: ', sum(1 for x in R_fin if x > (Rb + L))
    )

    pairs = [(ri, rf) for ri, rf in zip(R_ini, R_fin) if rf > Rb + L]
    R_ini = [p[0] for p in pairs]
    R_fin = [p[1] for p in pairs]

    print(mean(R_ini), stdev(R_ini))

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
    plt.xlim([0, 100])

    plt.xlabel('Distance from bubble center (nm)')
    plt.ylabel('Frequency')

    plt.legend()
    plt.savefig('/'.join(disp_file.split('/')[:-1] + ['xe_hist.pdf']))

def main():
    file_root = sys.argv[1]
    disp_file = file_root + '_displacements.output'
    toml_file = file_root + '.toml'
    xe_file = file_root + '_xenon_disp.output'

    calc(disp_file, toml_file, xe_file)

if __name__ == '__main__':
    main()
