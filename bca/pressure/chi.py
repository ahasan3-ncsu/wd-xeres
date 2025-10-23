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

def get_chi(P, en, rad, ion):
    rxe = []
    chi = []

    for pres in P:
        if pres == 1.0:
            subdirpath = f'../headon/{rad}nm/{ion}_{en:.1f}MeV'
        else:
            subdirpath = f'{rad}nm/{ion}_{en:.1f}MeV/p{pres:.1f}'

        if not os.path.exists(subdirpath):
            raise ValueError('fix your shit')

        with open(os.path.join(subdirpath, 'xe_res.json')) as f:
            foo = json.load(f)

        nxe = total_xe(rad * 10) * pres
        print(nxe)

        rxe.append(
            float(foo['re-solved'])
            / float(foo['sim_runs']) / 1e3    # 1e3 ions/sim_run
        )

        chi.append(
            float(foo['re-solved'])
            / float(foo['sim_runs']) / 1e3    # 1e3 ions/sim_run
            / nxe
        )

    return rxe, chi

def main():
    radii = [8, 64]

    Y_en = [1, 20]
    I_en = [1, 20]

    P = [0.8, 1.0, 1.2, 1.4]

    for rad in radii:
        # yttrium
        for y_e in Y_en:
            Y_rxe, Y_chi = get_chi(P, y_e, rad, 'Y')
            Y_dict = {'P': P, 'rxe': Y_rxe, 'chi': Y_chi}

            with open(f'data/{rad}nm_Y_{y_e:.1f}MeV.json', 'w') as f:
                json.dump(Y_dict, f, indent=4)

        # iodine
        for i_e in I_en:
            I_rxe, I_chi = get_chi(P, i_e, rad, 'I')
            I_dict = {'P': P, 'rxe': I_rxe, 'chi': I_chi}

            with open(f'data/{rad}nm_I_{i_e:.1f}MeV.json', 'w') as f:
                json.dump(I_dict, f, indent=4)

    return True

if __name__ == '__main__':
    main()
