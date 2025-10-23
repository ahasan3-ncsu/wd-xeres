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

def get_chi(L, en, rad, ion):
    chi = []

    for l in L:
        if l:
            subdirpath = f'{rad}nm/{ion}_{en:.1f}MeV/l{l/10:.0f}nm'
        else:
            subdirpath = f'../headon/{rad}nm/{ion}_{en:.1f}MeV'

        if not os.path.exists(subdirpath):
            raise ValueError('fix your shit')

        with open(os.path.join(subdirpath, 'xe_res.json')) as f:
            foo = json.load(f)

        chi.append(float(foo['re-solved']) / float(foo['sim_runs']))

    nxe = total_xe(rad * 10)
    print(nxe)
    chi = [c / 1e3 / nxe for c in chi]

    return chi

def main():
    radii = [8, 32, 64]

    Y_en = []
    I_en = [1, 10, 20]

    for rad in radii:
        Rb = rad * 10
        D = Rb + 1000
        L = [0, Rb // 2] + list(range(Rb, D, 250))

        # yttrium
        for y_e in Y_en:
            Y_chi = get_chi(L, y_e, rad, 'Y')
            Y_dict = {'L': L + [D], 'chi': Y_chi + [0.0]}

            with open(f'data/{rad}nm_Y_{y_e:.1f}MeV.json', 'w') as f:
                json.dump(Y_dict, f, indent=4)

        # iodine
        for i_e in I_en:
            I_chi = get_chi(L, i_e, rad, 'I')
            I_dict = {'L': L + [D], 'chi': I_chi + [0.0]}

            with open(f'data/{rad}nm_I_{i_e:.1f}MeV.json', 'w') as f:
                json.dump(I_dict, f, indent=4)

    return True

if __name__ == '__main__':
    main()
