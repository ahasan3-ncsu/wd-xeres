import os
import json
import matplotlib.pyplot as plt

def txe(rad, nrho):
    # angstrom only
    pi = 3.1415926535
    return 4 / 3 * pi * rad**3 * nrho

def main():
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

    for rad in radii:
        dirpath = f'{rad}nm'

        ### YTTRIUM
        chi = []
        for y_e in Y_en:
            subdirpath = f'{rad}nm/Y_{y_e:.1f}MeV'
            if not os.path.exists(subdirpath):
                raise ValueError('fix your shit')

            with open(os.path.join(subdirpath, 'xe_res.json')) as f:
                foo = json.load(f)

            chi.append(float(foo['re-solved']) / float(foo['sim_runs']))

        print(txe(rad * 10, n_eq[rad]))
        chi = [c / 1e3 / txe(rad * 10, n_eq[rad]) for c in chi]
        plt.plot(Y_en, chi, marker='o', label=f'{rad}nm')

        plt.title('Yttrium')
        plt.legend()
        plt.show()

        ### IODINE
        chi = []
        for i_e in I_en:
            subdirpath = f'{rad}nm/I_{i_e:.1f}MeV'
            if not os.path.exists(subdirpath):
                raise ValueError('fix your shit')

            with open(os.path.join(subdirpath, 'xe_res.json')) as f:
                foo = json.load(f)

            chi.append(float(foo['re-solved']) / float(foo['sim_runs']))

        print(txe(rad * 10, n_eq[rad]))
        chi = [c / 1e3 / txe(rad * 10, n_eq[rad]) for c in chi]
        plt.plot(I_en, chi, marker='o', label=f'{rad}nm')

        plt.title('Iodine')
        plt.legend()
        plt.show()

    return True

if __name__ == '__main__':
    main()
