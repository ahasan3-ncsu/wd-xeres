import sys
import numpy as np

def calc(eloss_file):
    jar = np.loadtxt(eloss_file, delimiter=',')

    E_nuke = jar[:, 2]
    E_elec = jar[:, 3]

    del jar

    nuke = E_nuke.sum()
    elec = E_elec.sum()

    print('Nuke: ', nuke)
    print('Elec: ', elec)

    print('Total: ', nuke + elec)
    print('Nuke ratio: ', nuke / (nuke + elec))
    print('Elec ratio: ', elec / (nuke + elec))

def main():
    file_root = sys.argv[1]
    eloss_file = file_root + '_energy_loss.output'
    print(eloss_file)

    calc(eloss_file)

if __name__ == '__main__':
    main()
