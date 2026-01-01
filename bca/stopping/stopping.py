import sys
import json
import numpy as np
import matplotlib.pyplot as plt

def create_vis(json_file, which_ion):
    with open(json_file, 'r') as f:
        jar = json.load(f)

    num_ions = jar['num_ions']
    bin_x = np.array(jar['bin_x'])
    bin_width = bin_x[1] - bin_x[0]
    nuke_loss = np.array(jar['nuke'])
    elec_loss = np.array(jar['elec'])

    k = 3
    for i in range(len(bin_x)//k):
        bin_x[i] = sum([bin_x[k*i+j] for j in range(k)]) / k
        nuke_loss[i] = sum([nuke_loss[k*i+j] for j in range(k)]) / k
        elec_loss[i] = sum([elec_loss[k*i+j] for j in range(k)]) / k

    first_zero = 0
    for i, v in enumerate(nuke_loss):
        if v == 0.0 and elec_loss[i] == 0.0:
            first_zero = i
            break

    bin_x = bin_x[:first_zero+1]
    nuke_loss = nuke_loss[:first_zero+1]
    elec_loss = elec_loss[:first_zero+1]

    plt.figure(figsize=(5, 4))

    plt.plot(
        bin_x / 1e4, # ang -> micron
        nuke_loss / num_ions / bin_width / 1e2, # eV/ang -> keV/nm
        label='Nuclear',
        # marker='o',
        # markersize=3,
        color=plt.cm.jet(0.8)
    )
    plt.plot(
        bin_x / 1e4, # ang -> micron
        elec_loss / num_ions / bin_width / 1e2, # eV/ang -> keV/nm
        label='Electronic',
        # marker='^',
        # markersize=3,
        ls='--',
        color=plt.cm.jet(0.2)
    )

    plt.xlim([0, 9])
    plt.ylim([0, 20])

    if which_ion == 'Y':
        plt.title(r'$^{97}_{39}$Y, 101.3 MeV')
    elif which_ion == 'I':
        plt.title(r'$^{136}_{53}$I, 74.6 MeV')

    plt.xlabel(r'Distance ($\mu$m)')
    plt.ylabel(r'Stopping power (keV/nm)')

    plt.legend()
    plt.tight_layout()
    plt.savefig('/'.join(json_file.split('/')[:-1] + [f'{which_ion}_stopping.pdf']))

def main():
    file_root = sys.argv[1]
    json_file = file_root + '_eloss_bin.json'
    which_ion = sys.argv[2]

    create_vis(json_file, which_ion)

if __name__ == '__main__':
    main()
