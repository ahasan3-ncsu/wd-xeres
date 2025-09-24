import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt

def pfn(col, prop):
    match prop:
        case 'n':
            return col['num_ions']
        case 'e':
            return np.mean(col['energies'])
        case 'a':
            return np.mean(col['angles'])
        case 'p':
            return col['num_ions'] / col['volume']
        case _:
            raise ValueError('Weird property! Use n, e, a, or p.')

def plot_grid(grid_file, prop):
    with open(grid_file, 'rb') as f:
        grid_data = pickle.load(f)

    ion_data = [
        [pfn(col, prop) for col in row]
        for row in grid_data
    ]
    t_data = np.array(ion_data).T

    plt.imshow(t_data,
               cmap='turbo',
               origin='lower',
               norm=('log' if prop=='p' else 'linear'))
    plt.colorbar()

    plt.show()

def main():
    file_root = sys.argv[1]
    data_file = file_root + '_grid_data.output'
    grid_prop = sys.argv[2]

    plot_grid(data_file, grid_prop)

if __name__ == '__main__':
    main()
