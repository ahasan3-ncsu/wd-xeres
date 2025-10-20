import sys
import json
import pickle
import numpy as np
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm

def extract_grid(grid_file):
    with open(grid_file, 'rb') as f:
        grid_data = pickle.load(f)

    return grid_data

def add_prob(grid_data, grid_info):
    cell_size, num_rows, num_cols = (
        grid_info['cell_size'], grid_info['num_rows'], grid_info['num_cols']
    )

    total_ions = grid_data[0][0]['num_ions']
    for i in range(num_rows):
        for j in range(num_cols):
            surf_area = np.pi * ((j+1)**2 - j**2) * cell_size**2
            grid_data[i][j]['probability'] = (
                grid_data[i][j]['num_ions'] / total_ions / surf_area
            )

    return grid_data

def pchip_spline(json_file):
    with open(json_file, 'r') as f:
        jar = json.load(f)

    # E -> MeV; chi -> fraction
    return PchipInterpolator(jar['E'], jar['chi'])

def get_chi(spline, energy, l, Rb, delta):
    # convert to MeV; eliminate negatives
    chi_0 = max(0, spline(energy / 1e6))
    f_l = (1 + np.cos(np.pi * l/(Rb+delta))) / 2

    return chi_0 * f_l

def get_grid_points(x, w, alpha, Rb, delta, T):
    D = Rb + delta
    cos_a = np.cos(alpha)
    sin_a = np.sin(alpha)

    xp, wp = x  - D * cos_a, w  - D * sin_a
    p1, q1 = xp - D * sin_a, wp + D * cos_a
    p2, q2 = xp + D * sin_a, wp - D * cos_a

    points = []
    for t1 in T:
        p = p1 + t1 * (p2 - p1)
        q = q1 + t1 * (q2 - q1)
        for t2 in T:
            z = -D + t2 * (2 * D)
            # point in question: (p, q, z)
            # central point: (xp, wp, 0)
            _w = (q**2 + z**2) ** 0.5
            _l = ((p - xp)**2 + (q - wp)**2 + z**2) ** 0.5
            points.append((p, _w, _l))

    return points

def add_xi(grid_data, grid_info, spline, mesh_info):
    cell_size, num_rows, num_cols = (
        grid_info['cell_size'], grid_info['num_rows'], grid_info['num_cols']
    )
    Rb, delta, nel_mesh = (
        mesh_info['Rb'], mesh_info['delta'], mesh_info['nel_mesh']
    )
    T = np.linspace(0, 1, nel_mesh+1)
    T = (T[1:] + T[:-1]) / 2

    for i in range(num_rows):
        for j in range(num_cols):
            # no ion in these cells
            if not grid_data[i][j]['num_ions']:
                grid_data[i][j]['xi'] = 0
                continue

            x, w = i * cell_size, j * cell_size
            alpha = grid_data[i][j]['angles']
            points = get_grid_points(x, w, alpha, Rb, delta, T)

            sum = 0.0
            for p in points:
                xp, wp, lp = p
                ip, jp = max(0, int(xp / cell_size)), int(wp / cell_size)
                # better corner case impl. needed
                # for now, remove elements with notably different angles
                if abs(grid_data[ip][jp]['angles']- alpha) > 0.2:
                    continue

                sum += (
                    grid_data[ip][jp]['probability']
                    * get_chi(
                            spline,
                            grid_data[ip][jp]['energies'],
                            lp, Rb, delta
                        )
                )

            sum *= (2*(Rb+delta) / nel_mesh) ** 2 / np.cos(alpha)
            grid_data[i][j]['xi'] = sum

    # ff origin cannot be inside the bubble
    for i in range(Rb // cell_size + 1):
        grid_data[i][0]['xi'] = 0

    return grid_data

def add_db(grid_data, grid_info):
    cell_size, num_rows, num_cols = (
        grid_info['cell_size'], grid_info['num_rows'], grid_info['num_cols']
    )

    b = 0.0
    for i in range(num_rows):
        for j in range(num_cols):
            surf_area = np.pi * ((j+1)**2 - j**2) * cell_size**2
            grid_data[i][j]['db'] = (
                grid_data[i][j]['xi']
                * surf_area * cell_size
            )
            b += grid_data[i][j]['db']

    print(b * 1e-30) # b/Fdot; angstrom^3 -> m^3
    return grid_data

def plot_prop(grid_data, prop, pnorm):
    prop_data = [
        [col[prop] for col in row]
        for row in grid_data
    ]
    t_data = np.array(prop_data).T

    plt.imshow(t_data,
               cmap='nipy_spectral',
               origin='lower',
               norm=pnorm)
    plt.colorbar()
    plt.show()

def main():
    rad = sys.argv[1]
    ion = sys.argv[2]

    json_file = f'data/{rad}nm_{ion}.json'
    grid_file = f'data/{ion}_surface_grid.output'

    print(json_file)
    print(grid_file)

    # ANGSTROM
    grid_info = {
        'cell_size': 500,
        'num_rows' : 180,
        'num_cols' : 100,
    }
    mesh_info = {
        'Rb'      : int(rad) * 10,
        'delta'   : 1000,
        'nel_mesh': 3,
    }

    spline = pchip_spline(json_file)

    grid = extract_grid(grid_file)
    grid = add_prob(grid, grid_info)
    grid = add_xi(grid, grid_info, spline, mesh_info)
    grid = add_db(grid, grid_info)

    # plot_prop(grid, 'probability', SymLogNorm(linthresh=1e-11))
    # plot_prop(grid, 'energies', 'linear')

    plot_prop(grid, 'xi', SymLogNorm(linthresh=1e-12))
    plot_prop(grid, 'db', SymLogNorm(linthresh=1e-2))

if __name__ == '__main__':
    main()
