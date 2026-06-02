import sys
import json
import numpy as np
import matplotlib.pyplot as plt

from stat_util import get_mean, get_std

def create_vis(json_file, which_ion):
    with open(json_file, 'r') as f:
        jar = json.load(f)

    num_ions = np.array(jar['num_ions'])
    bin_x = np.array(jar['bin_x'])
    nuke = np.array(jar['nuke'])
    cum_nuke = np.cumsum(nuke, axis=0)

    nuke_mean = np.array([get_mean(num_ions, i) for i in nuke])
    nuke_std = np.array([get_std(num_ions, i) for i in nuke])

    cum_nuke_mean = np.array([get_mean(num_ions, i) for i in cum_nuke])
    cum_nuke_std = np.array([get_std(num_ions, i) for i in cum_nuke])

    plt.style.use('../science.mplstyle')

    plt.plot(
        bin_x / 1e4, # ang -> micron
        nuke_mean / 1e6, # eV -> MeV
        label='Local',
        color='red'
    )
    plt.fill_between(
        bin_x / 1e4, # ang -> micron
        nuke_mean / 1e6 - nuke_std / 1e6, # eV -> MeV
        nuke_mean / 1e6 + nuke_std / 1e6, # eV -> MeV
        color='red',
        alpha=0.2
    )

    plt.plot(
        bin_x / 1e4, # ang -> micron
        cum_nuke_mean / 1e6, # eV -> MeV
        label='Cumulative',
        ls='-.',
        color='peru'
    )
    plt.fill_between(
        bin_x / 1e4, # ang -> micron
        cum_nuke_mean / 1e6 - cum_nuke_std / 1e6, # eV -> MeV
        cum_nuke_mean / 1e6 + cum_nuke_std / 1e6, # eV -> MeV
        color='peru',
        alpha=0.2
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
