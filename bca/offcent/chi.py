import os
import json
import matplotlib.pyplot as plt

def total_xe(rad):
    # ANGSTROM only
    pi = 3.1415926535

    # equilibrium number density for a radius
    n_eq = {
        10: 0.01152,
        20: 0.01129,
        40: 0.01086,
        80: 0.01008,
        160: 0.00881,
        320: 0.00704,
        640: 0.00503,
        1280: 0.00320
    }

    return 4 / 3 * pi * rad**3 * n_eq[rad]

def get_chi(E, l, rad, ion):
    chi = []

    for en in E:
        if l:
            subdirpath = f'{rad}nm/{ion}_{en:.1f}MeV/l{l/10:.0f}nm'
        else:
            subdirpath = f'../headon/{rad}nm/{ion}_{en:.1f}MeV'

        if not os.path.exists(subdirpath):
            raise ValueError(f'fix your shit: {subdirpath}')

        with open(os.path.join(subdirpath, 'xe_res.json')) as f:
            foo = json.load(f)

        chi.append(float(foo['re-solved']) / float(foo['sim_runs']))

    nxe = total_xe(rad * 10)
    print(nxe)
    chi = [c / 1e3 / nxe for c in chi]

    return chi

def main():
    Y_en = [0.1, 0.5, 1, 2, 5, 10, 20, 40, 60, 80, 102]
    I_en = [0.1, 0.5, 1, 2, 5, 10, 20, 40, 60, 75]

    radii = [1, 2, 4, 8, 16, 32, 64, 128]

    # sync with off_dissem
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

    for rad in radii:
        # prepend 0 to get headon data when looping
        Lloc = [0] + L[rad]

        # yttrium
        Y_chi = []
        for l in Lloc:
            Y_chi.append(get_chi(Y_en, l, rad, 'Y'))

        Y_dict = {
            'L': Lloc,
            'E': Y_en,
            'chi': Y_chi
        }
        with open(f'data/{rad}nm_Y.json', 'w') as f:
            json.dump(Y_dict, f, indent=4)

        # iodine
        I_chi = []
        for l in Lloc:
            I_chi.append(get_chi(I_en, l, rad, 'I'))

        I_dict = {
            'L': Lloc,
            'E': I_en,
            'chi': I_chi
        }
        with open(f'data/{rad}nm_I.json', 'w') as f:
            json.dump(I_dict, f, indent=4)

    return True

if __name__ == '__main__':
    main()
