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
    Y_en = [0.1, 0.5, 1, 2, 5, 10, 20, 40, 60, 80, 102]
    I_en = [0.1, 0.5, 1, 2, 5, 10, 20, 40, 60, 75]

    # only intergranular bubbles for now
    radii = [8, 16, 32, 64, 128]

    for rad in radii:
        # yttrium
        Y_chi = get_chi(Y_en, rad, 'Y')
        Y_dict = {'E': Y_en, 'chi': Y_chi}

        with open(f'data/{rad}nm_Y.json', 'w') as f:
            json.dump(Y_dict, f, indent=4)

        # iodine
        I_chi = get_chi(I_en, rad, 'I')
        I_dict = {'E': I_en, 'chi': I_chi}

        with open(f'data/{rad}nm_I.json', 'w') as f:
            json.dump(I_dict, f, indent=4)

        # plot or not
        if False:
            plotter(Y_en, Y_chi, rad, 'Yttrium')
            plotter(I_en, I_chi, rad, 'Iodine')

    return True

if __name__ == '__main__':
    main()
