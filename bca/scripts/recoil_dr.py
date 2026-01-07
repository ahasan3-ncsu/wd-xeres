import sys
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('../science.mplstyle')

def create_vis(disp_file, save_ext):
    E = [[], [], []]
    D = [[], [], []]

    with open(disp_file, 'r') as f:
        for line in f:
            tmp = line.split(',')
            energ = float(tmp[2])
            dr2 = [(float(tmp[6+i]) - float(tmp[3+i]))**2 for i in range(3)]

            i = -1
            match int(tmp[1]):
                case 92:
                    i = 0
                case 42:
                    i = 1
                case 54:
                    i = 2
                case _:
                    raise ValueError('Weird atomic number!')

            E[i].append(energ)
            D[i].append(sum(dr2)**0.5 / 10) # converted to nm

    plt.scatter(E[0], D[0],
                marker='s', s=5, color=plt.cm.jet(0.8),
                label='U', rasterized=True)
    plt.scatter(E[1], D[1],
                marker='o', s=5, color=plt.cm.jet(0.2),
                label='Mo', rasterized=True)
    # plt.scatter(E[2], D[2],
    #             marker='D', s=5, color='yellow',
    #             label='Xe', rasterized=True)

    plt.xscale('log')
    plt.yscale('log')

    plt.xlim([1e1, 3e6])
    plt.ylim([0.3, 3e2])

    plt.xlabel('Recoil energy (eV)')
    plt.ylabel('Displacement (nm)')

    plt.legend()
    plt.savefig(
        '/'.join(disp_file.split('/')[:-1] + [f'recoil_dr.{save_ext}']),
        dpi=500
    )

def main():
    file_root = sys.argv[1]
    disp_file = file_root + '_displacements.output'
    save_ext = sys.argv[2]

    create_vis(disp_file, save_ext)

if __name__ == '__main__':
    main()
