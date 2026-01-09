import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm

plt.rcParams.update({
    'text.usetex': True,
    'mathtext.fontset': 'cm'
})

def plot_prop(id, grid_data, prop, pnorm):
    prop_data = [
        [col[prop] for col in row]
        for row in grid_data
    ]
    t_data = np.array(prop_data).T

    if prop == 'db':
        t_data = t_data * 1e-30 # to make it m^3

    plt.figure(figsize=(6, 3))

    plt.imshow(t_data,
               cmap='nipy_spectral',
               origin='lower',
               extent=(0, 9, 0, 5),
               norm=pnorm)

    plt.xlabel(r'x ($\mu$m)', fontsize=12)
    plt.ylabel(r'w ($\mu$m)', fontsize=12)

    if prop == 'db':
        plt.colorbar(label=r'm$^3$')
    else:
        plt.colorbar()

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
    plot_prop(id, grid, 'db', SymLogNorm(linthresh=1e-32))

if __name__ == '__main__':
    main()
