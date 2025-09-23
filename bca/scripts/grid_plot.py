import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
from grid_gen import print_grid

def plot_grid(grid_file):
    with open(grid_file, 'rb') as f:
        grid_data = pickle.load(f)

    # print_grid(grid_data, 'num_ions')

    ion_data = [[col['num_ions'] for col in row] for row in grid_data]
    t_data = np.array(ion_data).T

    plt.imshow(t_data, cmap='turbo', origin='lower')
    plt.colorbar()

    plt.show()

def main():
    file_root = sys.argv[1]
    data_file = file_root + '_grid_data.output'

    plot_grid(data_file)

if __name__ == '__main__':
    main()
