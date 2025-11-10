import sys
import json
import numpy as np
import matplotlib.pyplot as plt

def create_vis(json_file, which_ion):
    with open(json_file, 'r') as f:
        jar = json.load(f)

    num_ions = jar['num_ions']
    bin_x = np.array(jar['bin_x'])
    nuke_loss = np.array(jar['nuke'])

    first_zero = 0
    for i, v in enumerate(nuke_loss):
        if v == 0.0:
            first_zero = i
            break

    bin_x = bin_x[:first_zero+1]
    nuke_loss = nuke_loss[:first_zero+1]
    cum_nuke_loss = np.cumsum(nuke_loss)

    plt.figure(figsize=(5, 4))

    plt.plot(
        bin_x / 1e4, # ang -> micron
        nuke_loss / num_ions / 1e6, # eV -> MeV
        label='Local',
        # marker='o',
        # markersize=3,
        color='red'
    )
    plt.plot(
        bin_x / 1e4, # ang -> micron
        cum_nuke_loss / num_ions / 1e6, # eV -> MeV
        label='Cumulative',
        # marker='s',
        # markersize=3,
        ls='-.',
        color='peru'
    )

    if which_ion == 'Y':
        plt.title(r'$^{97}_{39}Y$, 101.3 MeV')
    elif which_ion == 'I':
        plt.title(r'$^{136}_{53}I$, 74.6 MeV')

    plt.xlabel(r'Distance ($\mu$m)')
    plt.ylabel(r'Nuclear energy loss (MeV)')

    plt.legend()
    plt.savefig('/'.join(json_file.split('/')[:-1] + [f'{which_ion}_nuke_loss.pdf']))

def main():
    file_root = sys.argv[1]
    json_file = file_root + '_eloss_bin.json'
    which_ion = sys.argv[2]

    create_vis(json_file, which_ion)

if __name__ == '__main__':
    main()
