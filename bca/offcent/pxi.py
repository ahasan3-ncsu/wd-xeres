import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm

def plot_prop(id, grid_data, prop, pnorm):
    prop_data = [
        [col[prop] for col in row]
        for row in grid_data
    ]
    t_data = np.array(prop_data).T

    plt.figure(figsize=(6, 3))

    plt.imshow(t_data,
               cmap='nipy_spectral',
               origin='lower',
               extent=(0, 9, 0, 5),
               norm=pnorm)

    plt.xlabel(r'x ($\mu$m)')
    plt.ylabel(r'w ($\mu$m)')

    plt.colorbar()
    plt.tight_layout()
    plt.savefig(f'{id}_{prop}.pdf')

def main():
    rad = sys.argv[1]
    ion = sys.argv[2]

    id = f'{rad}nm_{ion}'
    grid_file = f'data/{id}_surface_grid.output'
    print(grid_file)

    with open(grid_file, 'rb') as f:
        grid = pickle.load(f)

    # plot_prop(grid, 'probability', SymLogNorm(linthresh=1e-11))
    # plot_prop(grid, 'energies', 'linear')

    plot_prop(id, grid, 'xi', SymLogNorm(linthresh=1e-12))
    plot_prop(id, grid, 'db', SymLogNorm(linthresh=1e-2))

if __name__ == '__main__':
    main()
