import os
import sys
import json
import tomllib
import numpy as np

def extract(eloss_file, json_file, toml_file, which_ion):
    jar = np.loadtxt(eloss_file, delimiter=',')

    x = jar[:, 4]
    E_nuke = jar[:, 2]
    E_elec = jar[:, 3]

    del jar

    bin_width = 1000
    x_min, x_max = 0, 90000

    bins = np.arange(x_min, x_max + bin_width, bin_width)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    num_bins = len(bin_centers) # should be 90

    nuke_loss_per_bin = np.zeros(len(bin_centers))
    elec_loss_per_bin = np.zeros(len(bin_centers))

    x_bin_ind = np.digitize(x, bins)
    np.add.at(nuke_loss_per_bin, x_bin_ind - 1, E_nuke)
    np.add.at(elec_loss_per_bin, x_bin_ind - 1, E_elec)

    with open(toml_file, 'rb') as f:
        foo = tomllib.load(f)

    if which_ion == 'Y':
        curr_n_ions = foo['particle_parameters']['N'][0]
    elif which_ion == 'I':
        curr_n_ions = foo['particle_parameters']['N'][1]
    else:
        raise ValueError('Wrong ion type!')

    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
    else:
        data = {
            'num_ions': 0,
            'bin_x':    bin_centers.tolist(),
            'nuke':     [0.0] * num_bins,
            'elec':     [0.0] * num_bins
        }

    data['num_ions'] += curr_n_ions
    for i in range(len(bin_centers)):
        data['nuke'][i] += float(nuke_loss_per_bin[i])
        data['elec'][i] += float(elec_loss_per_bin[i])

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    file_root = sys.argv[1]
    eloss_file = file_root + '_energy_loss.output'
    json_file = file_root + '_eloss_bin.json'
    toml_file = file_root + '.toml'
    which_ion = sys.argv[2]

    extract(eloss_file, json_file, toml_file, which_ion)

if __name__ == '__main__':
    main()
