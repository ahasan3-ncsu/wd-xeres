import sys
import json
import pickle
import numpy as np
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm

grid_size = int(5e2) # ANGSTROM
num_rows = int(9e4 / grid_size) # 9 micron
num_cols = int(5e4 / grid_size) # 5 micron
delta = 1000

def pchip_spline(json_file):
    with open(json_file, 'r') as f:
        jar = json.load(f)

    # E -> MeV; chi -> fraction
    return PchipInterpolator(jar['E'], jar['chi'])

def get_chi(spline, energy):
    mev = energy / 1e6
    chi = spline(mev)

    # eliminate negatives
    return max(0, chi)

def extract_grid(grid_file):
    with open(grid_file, 'rb') as f:
        grid_data = pickle.load(f)

    return grid_data

def add_prob(grid_data):
    total_ions = grid_data[0][0]['num_ions']
    for i in range(num_rows):
        for j in range(num_cols):
            surf_area = np.pi * ((j+1)**2 - j**2) * grid_size**2
            grid_data[i][j]['probability'] = (
                grid_data[i][j]['num_ions'] / total_ions / surf_area
            )

    return grid_data

def add_xi(grid_data, Rb, spline):
    for i in range(num_rows):
        for j in range(num_cols):
            grid_data[i][j]['xi'] = (
                grid_data[i][j]['probability']
                * (Rb + delta)**2
                * get_chi(spline, grid_data[i][j]['energies'])
            )

    return grid_data

def add_db(grid_data):
    b = 0.0
    for i in range(num_rows):
        for j in range(num_cols):
            surf_area = np.pi * ((j+1)**2 - j**2) * grid_size**2
            grid_data[i][j]['db'] = (
                grid_data[i][j]['xi']
                * surf_area * grid_size
            )
            b += grid_data[i][j]['db']

    print(b)
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

    spline = pchip_spline(json_file)

    grid = extract_grid(grid_file)
    grid = add_prob(grid)
    grid = add_xi(grid, int(rad) * 10, spline)
    grid = add_db(grid)

    # plot_prop(grid, 'probability', SymLogNorm(linthresh=1e-11))
    # plot_prop(grid, 'energies', 'linear')

    plot_prop(grid, 'xi', SymLogNorm(linthresh=1e-12))
    plot_prop(grid, 'db', SymLogNorm(linthresh=1e-2))

if __name__ == '__main__':
    main()
