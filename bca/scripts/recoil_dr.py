import sys
import numpy as np
import matplotlib.pyplot as plt

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
            D[i].append(sum(dr2)**0.5)

    plt.scatter(E[0], D[0],
                marker='s', s=5, color='red', label='U')
    plt.scatter(E[1], D[1],
                marker='o', s=5, color='blue', label='Mo')
    plt.scatter(E[2], D[2],
                marker='D', s=5, color='yellow', label='Xe')

    plt.xscale('log')
    plt.yscale('log')

    plt.xlabel('Recoil energy (eV)')
    plt.ylabel(r'Displacement ($\AA$)')

    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig('/'.join(disp_file.split('/')[:-1] + [f'recoil_dr.{save_ext}']))

def main():
    file_root = sys.argv[1]
    disp_file = file_root + '_displacements.output'
    save_ext = sys.argv[2]

    create_vis(disp_file, save_ext)

if __name__ == '__main__':
    main()
