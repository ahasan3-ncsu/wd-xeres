import os
import json
import matplotlib.pyplot as plt

def total_xe(rad):
    # ANGSTROM only
    pi = 3.1415926535

    # equilibrium number density for a radius (subject to change)
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

def get_chi(E, rad, ion):
    chi = []

    for en in E:
        subdirpath = f'{rad}nm/{ion}_{en:.1f}MeV'
        if not os.path.exists(subdirpath):
            raise ValueError('fix your shit')

        with open(os.path.join(subdirpath, 'xe_res.json')) as f:
            foo = json.load(f)

        chi.append(float(foo['re-solved']) / float(foo['sim_runs']))

    nxe = total_xe(rad * 10)
    print(nxe)
    chi = [c / 1e3 / nxe for c in chi]

    return chi

def plotter(E, chi, rad, ion):
    plt.plot(E, chi, marker='o', label=f'{rad}nm')

    plt.title(ion)
    plt.legend()
    plt.show()

def main():
    # energy discretization
    Y_en = [102, 80, 60, 40, 20, 10, 5, 2, 1, 0.5, 0.1]
    I_en = [75, 60, 40, 20, 10, 5, 2, 1, 0.5, 0.1]

    # only intergranular for now
    radii = [64, 128]

    for rad in radii:
        ### YTTRIUM
        plotter(Y_en, get_chi(Y_en, rad, 'Y'), rad, 'Yttrium')

        ### IODINE
        plotter(I_en, get_chi(I_en, rad, 'I'), rad, 'Iodine')

    return True

if __name__ == '__main__':
    main()
