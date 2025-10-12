import sys
import tomllib
import numpy as np
import matplotlib.pyplot as plt

def create_vis(eloss_file, toml_file, which_ion):
    jar = np.loadtxt(eloss_file, delimiter=',')

    x = jar[:, 4]
    E_nuke = jar[:, 2]

    del jar

    bin_width = 5000
    x_min, x_max = x.min(), x.max()

    bins = np.arange(x_min, x_max + bin_width, bin_width)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    nuke_loss_per_bin = np.zeros(len(bin_centers))

    x_bin_ind = np.digitize(x, bins)
    np.add.at(nuke_loss_per_bin, x_bin_ind - 1, E_nuke)
    cum_nuke_loss = np.cumsum(nuke_loss_per_bin)

    with open(toml_file, 'rb') as f:
        foo = tomllib.load(f)

    if which_ion == 'Y':
        num_ions = foo['particle_parameters']['N'][0]
    elif which_ion == 'I':
        num_ions = foo['particle_parameters']['N'][1]
    else:
        raise ValueError('Wrong ion type!')

    plt.figure(figsize=(5, 4))

    plt.plot(
        bin_centers / 1e4, # ang -> micron
        nuke_loss_per_bin / num_ions / 1e6, # eV -> MeV
        label='Local',
        marker='o',
        markersize=3,
        color='red'
    )
    plt.plot(
        bin_centers / 1e4, # ang -> micron
        cum_nuke_loss / num_ions / 1e6, # eV -> MeV
        label='Cumulative',
        marker='s',
        markersize=3,
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
    plt.savefig('/'.join(eloss_file.split('/')[:-1] + [f'{which_ion}_nuke_loss.pdf']))

def main():
    file_root = sys.argv[1]
    eloss_file = file_root + '_energy_loss.output'
    toml_file = file_root + '.toml'
    which_ion = sys.argv[2]

    create_vis(eloss_file, toml_file, which_ion)

if __name__ == '__main__':
    main()
