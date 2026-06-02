import sys
import json
import numpy as np
import matplotlib.pyplot as plt

from stat_util import get_mean, get_std

def create_vis(json_file, which_ion):
    with open(json_file, 'r') as f:
        jar = json.load(f)

    num_ions = jar['num_ions']
    bin_x = np.array(jar['bin_x'])
    bin_width = bin_x[1] - bin_x[0]
    nuke = np.array(jar['nuke'])
    elec = np.array(jar['elec'])

    nuke_mean = np.array([get_mean(num_ions, i) for i in nuke])
    nuke_std = np.array([get_std(num_ions, i) for i in nuke])

    elec_mean = np.array([get_mean(num_ions, i) for i in elec])
    elec_std = np.array([get_std(num_ions, i) for i in elec])

    first_zero = 0
    for i, v in enumerate(nuke_mean):
        if v == 0.0 and elec_mean[i] == 0.0:
            first_zero = i
            break

    k = 3
    arrays = [bin_x, nuke_mean, nuke_std, elec_mean, elec_std]
    for i in range(len(bin_x) // k):
        for arr in arrays:
            arr[i] = sum(arr[k*i + j] for j in range(k)) / k

    arrays = [arr[:first_zero // k + 1] for arr in arrays]
    bin_x, nuke_mean, nuke_std, elec_mean, elec_std = arrays

    plt.style.use('../science.mplstyle')

    plt.plot(
        bin_x / 1e4, # ang -> micron
        nuke_mean / bin_width / 1e2, # eV/ang -> keV/nm
        label='Nuclear',
        color=plt.cm.jet(0.8)
    )
    plt.fill_between(
        bin_x / 1e4,
        nuke_mean / bin_width / 1e2 - 2 * nuke_std / bin_width / 1e2,
        nuke_mean / bin_width / 1e2 + 2 * nuke_std / bin_width / 1e2,
        lw=0,
        color=plt.cm.jet(0.8),
        alpha=0.3
    )

    plt.plot(
        bin_x / 1e4, # ang -> micron
        elec_mean / bin_width / 1e2, # eV/ang -> keV/nm
        ls='--',
        label='Electronic',
        color=plt.cm.jet(0.2)
    )
    plt.fill_between(
        bin_x / 1e4,
        elec_mean / bin_width / 1e2 - 2 * elec_std / bin_width / 1e2,
        elec_mean / bin_width / 1e2 + 2 * elec_std / bin_width / 1e2,
        lw=0,
        color=plt.cm.jet(0.2),
        alpha=0.3
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
    plt.savefig('/'.join(json_file.split('/')[:-1] + [f'{which_ion}_stopping.pdf']))

def main():
    file_root = sys.argv[1]
    json_file = file_root + '_eloss_bin.json'
    which_ion = sys.argv[2]

    create_vis(json_file, which_ion)

if __name__ == '__main__':
    main()
