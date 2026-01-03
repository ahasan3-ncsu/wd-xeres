import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm

def pfn(col, prop):
    match prop:
        case 'n':
            return col['num_ions']
        case 'e':
            return np.mean(col['energies']) if col['energies'] else 0
        case 'a':
            return np.mean(col['angles']) if col['angles'] else 0
        case _:
            raise ValueError('Weird property! Use n, e, a, or p.')

def plot_grid(grid_file, prop):
    with open(grid_file, 'rb') as f:
        grid_data = pickle.load(f)

    if prop == 'p':
        grid_size = int(50) # 50 nm should be enough
        num_rows = int(9e3 / grid_size) # 9 micron in width
        num_cols = int(5e3 / grid_size) # 5 micron in height

        ion_data = [
            [0 for col in row]
            for row in grid_data
        ]

        total_ions = grid_data[0][0]['num_ions']
        for i in range(num_rows):
            for j in range(num_cols):
                surf_area = np.pi * ((j+1)**2 - j**2) * grid_size**2
                ion_data[i][j] = grid_data[i][j]['num_ions'] / total_ions / surf_area

        t_data = np.array(ion_data).T
        pnorm = SymLogNorm(linthresh=1e-9)
    else:
        ion_data = [
            [pfn(col, prop) for col in row]
            for row in grid_data
        ]

        t_data = np.array(ion_data).T
        pnorm = 'linear'

    plt.figure(figsize=(6, 3))

    # option 1: imshow
    plt.imshow(t_data,
               cmap='nipy_spectral',
               origin='lower',
               extent=(0, 9, 0, 5),
               norm=pnorm)

    # option 2: pcolormesh
    # x_edges = np.linspace(0, 9, 181)
    # w_edges = np.linspace(0, 5, 101)
    # X, W = np.meshgrid(x_edges, w_edges)
    # plt.pcolormesh(X, W, t_data,
    #                cmap='nipy_spectral',
    #                norm=pnorm)

    plt.xlabel(r'x ($\mu$m)', fontsize=12)
    plt.ylabel(r'w ($\mu$m)', fontsize=12)

    match prop:
        case 'e':
            cbar_label = 'eV'
        case 'a':
            cbar_label = 'rad'
        case 'p':
            cbar_label = r'nm$^{-2}$'
        case _:
            cbar_label = ''

    plt.colorbar(label=cbar_label)
    plt.savefig(f'{grid_file[-21]}_{prop}.pdf')

def main():
    file_root = sys.argv[1]
    data_file = file_root + '_surface_grid.output'
    grid_prop = sys.argv[2]

    plot_grid(data_file, grid_prop)

if __name__ == '__main__':
    main()
