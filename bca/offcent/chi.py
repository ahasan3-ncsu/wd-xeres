import os
import json
import matplotlib.pyplot as plt

def total_xe(rad):
    # ANGSTROM only
    pi = 3.1415926535

    # equilibrium number density for a radius
    n_eq = {
        10: 0.00905,
        20: 0.00908,
        40: 0.01009,
        80: 0.00868,
        160: 0.00662,
        320: 0.00479,
        640: 0.00327,
        1280: 0.00209
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
    radii = [8, 16, 32, 64, 128]

    Y_en = [0.1, 0.5, 1, 2, 5, 10, 20, 40, 60, 80, 102]
    I_en = [0.1, 0.5, 1, 2, 5, 10, 20, 40, 60, 75]

    for rad in radii:
        D = rad * 10 + 1000
        L = [0] + [i * D // 4 for i in range(1, 4)]

        # yttrium
        Y_chi = []
        for l in L:
            Y_chi.append(get_chi(Y_en, l, rad, 'Y'))

        Y_chi.append([0.0] * len(Y_en))
        Y_dict = {'L': L + [D], 'E': Y_en, 'chi': Y_chi}
        with open(f'data/{rad}nm_Y.json', 'w') as f:
            json.dump(Y_dict, f, indent=4)

        # iodine
        I_chi = []
        for l in L:
            I_chi.append(get_chi(I_en, l, rad, 'I'))

        I_chi.append([0.0] * len(I_en))
        I_dict = {'L': L + [D], 'E': I_en, 'chi': I_chi}
        with open(f'data/{rad}nm_I.json', 'w') as f:
            json.dump(I_dict, f, indent=4)

    return True

if __name__ == '__main__':
    main()
