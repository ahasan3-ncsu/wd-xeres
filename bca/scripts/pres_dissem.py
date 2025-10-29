import os
import shutil
import subprocess
from input_gen import gen_toml

def irun(idict, ipath):
    # make input.toml file
    ifile = gen_toml(idict)

    # move input file
    os.makedirs(ipath)
    shutil.move(ifile, ipath)

    # run sim, get xe_res number
    subprocess.run(['python', 'runner.py', ipath, '2'])
    # aggregate xe_res, test convergence
    subprocess.run(['python', 'agg.py', ipath])

    return True

def main():
    # equilibrium number density for a radius (vdW EOS)
    n_eq = {
        1: 0.01152,
        2: 0.01129,
        4: 0.01086,
        8: 0.01008,
        16: 0.00881,
        32: 0.00704,
        64: 0.00503,
        128: 0.00320
    }

    # energy discretization
    Y_en = [1, 20]
    I_en = [1, 20]

    # only intergranular for now
    radii = [8, 64]

    # different pressures
    pres_mult = [0.8, 1.2, 1.4]

    arg_dict = {'filename': 'ballbox.toml'}

    for rad in radii:
        dirpath = f'{rad}nm'
        os.makedirs(dirpath, exist_ok=True)

        for y_e in Y_en:
            for mult in pres_mult:
                subdirpath = f'{rad}nm/Y_{y_e:.1f}MeV/p{mult:.1f}'
                if os.path.exists(subdirpath):
                    continue

                arg_dict['sphere'] = [rad * 10, n_eq[rad] * mult]
                arg_dict['yttrium'] = [1000, y_e * 1e6, 0.0]
                arg_dict['iodine'] = [0, 0.0, 0.0]

                irun(arg_dict, subdirpath)

        for i_e in I_en:
            for mult in pres_mult:
                subdirpath = f'{rad}nm/I_{i_e:.1f}MeV/p{mult:.1f}'
                if os.path.exists(subdirpath):
                    continue

                arg_dict['sphere'] = [rad * 10, n_eq[rad] * mult]
                arg_dict['yttrium'] = [0, 0.0, 0.0]
                arg_dict['iodine'] = [1000, i_e * 1e6, 0.0]

                irun(arg_dict, subdirpath)

    return True

if __name__ == '__main__':
    main()
