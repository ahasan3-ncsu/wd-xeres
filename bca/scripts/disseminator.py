import os
import shutil
from input_gen import gen_toml

# equilibrium number density for a radius (subject to change)
n_eq = {
    1: 0.00905,
    2: 0.00908,
    4: 0.01009,
    8: 0.00868,
    16: 0.00662,
    32: 0.00479,
    64: 0.00327,
    128: 0.00209
}

# energy discretization
Y_en = [102, 80, 60, 40, 20, 10, 5, 2, 1, 0.5, 0.1]
I_en = [75, 60, 40, 20, 10, 5, 2, 1, 0.5, 0.1]

# only intergranular for now
radii = [64, 128]

arg_dict = {'filename': 'ballbox.toml'}

for rad in radii:
    arg_dict['sphere'] = [rad * 10, n_eq[rad]]

    os.makedirs(f'{rad}nm', exist_ok=True)

    for y_e in Y_en:
        # check if the directory exists already
        # continue to the next energy if it does
        # this will enable getting incremental discrete values

        arg_dict['yttrium'] = [1000, y_e * 1e6, 0.0]
        arg_dict['iodine'] = [0, 0.0, 0.0]

        # make input.toml file
        input_file = gen_toml(arg_dict)


        # move input file
        os.makedirs(f'{rad}nm/Y_{y_e}MeV', exist_ok=True)
        shutil.move(input_file, f'{rad}nm/Y_{y_e}MeV/')

        # use a runner.py-like script to do sims (do 5 runs)
        # run agg.py-like script to check for convergence (check error)

    for i_e in I_en:
        # check if the directory exists already
        # continue to the next energy if it does
        # this will enable getting incremental discrete values

        arg_dict['yttrium'] = [0, 0.0, 0.0]
        arg_dict['iodine'] = [1000, i_e * 1e6, 0.0]

        # make input.toml file
        input_file = gen_toml(arg_dict)

        # move input file
        os.makedirs(f'{rad}nm/I_{i_e}MeV', exist_ok=True)
        shutil.move(input_file, f'{rad}nm/I_{i_e}MeV/')

        # use a runner.py-like script to do sims (do 5 runs)
        # run agg.py-like script to check for convergence (check error)
