import os
import copy
import pickle
import numpy as np

def get_sim_dir(prefix='run_'):
    i = 1
    while True:
        yield f'{prefix}{i}'
        i += 1

def make_grid(rows, cols):
    grid = [
        [
            {
                'num_ions': 0,     # integer
                'energies': 0.0,   # eV
                'angles': 0.0      # radian (0 -> pi/2)
            }
            for _ in range(cols)
        ]
        for _ in range(rows)
    ]

    return grid

def process_output(output_path, master_grid):
    nrows = len(master_grid)
    ncols = len(master_grid[0])

    with open(output_path, 'rb') as f:
        output_grid = pickle.load(f)

    ret_grid = make_grid(nrows, ncols)

    for i in range(nrows):
        for j in range(ncols):
            ret = ret_grid[i][j]
            mas = master_grid[i][j]
            out = output_grid[i][j]

            nion_mas = mas['num_ions']
            nion_out = out['num_ions']

            ret['num_ions'] = nion_mas + nion_out
            if (nion_mas + nion_out):
                ret['energies'] = ( (mas['num_ions'] * mas['energies'] + np.sum(out['energies']))
                    / (mas['num_ions'] + out['num_ions']) )
                ret['angles'] = ( (mas['num_ions'] * mas['angles'] + np.sum(out['angles']))
                    / (mas['num_ions'] + out['num_ions']) )

    return ret_grid

def get_mean(arr):
    return np.mean(arr) if arr else 1e-6

def diff_grids(A, B, points):
    diff = 0.0

    for p in points:
        i, j = p

        if B[i][j]['num_ions'] and A[i][j]['num_ions']:
            n_diff = ( (B[i][j]['num_ions'] / B[0][0]['num_ions'])
                / (A[i][j]['num_ions'] / A[0][0]['num_ions']) ) - 1
            diff = max(diff, abs(n_diff))

        e_diff = get_mean(B[i][j]['energies']) / get_mean(A[i][j]['energies']) - 1
        diff = max(diff, abs(e_diff))

        a_diff = get_mean(B[i][j]['angles']) / get_mean(A[i][j]['angles']) - 1
        diff = max(diff, abs(a_diff))

    return diff

def main():
    grid_size = int(5e2) # 50 nm should be enough
    num_rows = int(9e4 / grid_size) # 9 micron in width
    num_cols = int(5e4 / grid_size) # 5 micron in height

    old_grid = make_grid(num_rows, num_cols)
    new_grid = make_grid(num_rows, num_cols)

    dir_gen = get_sim_dir()

    poi = [(60, 0), (100, 0), (140, 0), (90, 10), (130, 10), (120, 20)]
    # poi = [(40, 0), (70, 0), (100, 0), (60, 10), (90, 10), (80, 20)]
    diff = 1.0

    while diff > 1e-3:
    # for _ in range(5):
        output_file = 'umo_0D_surface_grid.output'
        output_path = os.path.join(next(dir_gen), output_file)
        if not os.path.exists(output_path):
            break

        new_grid = process_output(output_path, old_grid)
        diff = diff_grids(old_grid, new_grid, poi)
        print('DIFF: ', diff)

        old_grid = copy.deepcopy(new_grid)

    with open('Y_surface_grid.output', 'wb') as f:
    # with open('I_surface_grid.output', 'wb') as f:
        pickle.dump(new_grid, f)

if __name__ == '__main__':
    main()
