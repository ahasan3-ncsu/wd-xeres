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
    subprocess.run(['python', 'runner.py', ipath, '3'])
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

    Y_en = [0.1, 0.5, 1, 2, 5, 10, 20, 40, 60, 80, 102]
    I_en = [0.1, 0.5, 1, 2, 5, 10, 20, 40, 60, 75]

    radii = [1, 2, 4, 8, 16, 32, 64, 128]

    L = {
        1: [10, 20, 63, 126, 189, 252, 505, 757, 1010],
        2: [20, 40, 63, 127, 191, 255, 510, 765, 1020],
        4: [40, 65, 80, 130, 195, 260, 520, 780, 1040],
        8: [67, 80, 135, 160, 202, 270, 540, 810, 1080],
        16: [145, 160, 290, 320, 580, 870, 1160],
        32: [330, 495, 660, 990, 1320],
        64: [410, 640, 820, 1230, 1640],
        128: [570, 1140, 1425, 1710, 2280]
    }

    arg_dict = {'filename': 'ballbox.toml'}

    for rad in radii:
        arg_dict['sphere'] = [rad * 10, n_eq[rad]]

        dirpath = f'{rad}nm'
        os.makedirs(dirpath, exist_ok=True)

        for y_e in Y_en:
            for l in L[rad]:
                subdirpath = f'{rad}nm/Y_{y_e:.1f}MeV/l{l/10:.0f}nm'
                if os.path.exists(subdirpath):
                    continue

                arg_dict['yttrium'] = [1000, y_e * 1e6, l]
                arg_dict['iodine'] = [0, 0.0, l]

                irun(arg_dict, subdirpath)

        for i_e in I_en:
            for l in L[rad]:
                subdirpath = f'{rad}nm/I_{i_e:.1f}MeV/l{l/10:.0f}nm'
                if os.path.exists(subdirpath):
                    continue

                arg_dict['yttrium'] = [0, 0.0, l]
                arg_dict['iodine'] = [1000, i_e * 1e6, l]

                irun(arg_dict, subdirpath)

    return True

if __name__ == '__main__':
    main()
