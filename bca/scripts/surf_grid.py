import sys
import pickle
import numpy as np

def make_grid(rows, cols):
    grid = [
        [
            {
                'surf_area': 0.0,  # angstrom^2
                'num_ions': 0,     # integer
                'energies': [],    # eV
                'angles': []       # radian (0 -> pi/2)
            }
            for _ in range(cols)
        ]
        for _ in range(rows)
    ]

    for i in range(rows):
        for j in range(cols):
            # 1e6 is there to make it angstrom^2
            grid[i][j]['surf_area'] = np.pi * ((j+1)**2 - j**2) * 1e6

    return grid

def extract_from_traj(row_file, xyz_file, grid, grid_sz):
    # number of rows for ions
    p_rows = np.loadtxt(row_file, dtype=int)

    # needed for out-of-bounds ions
    nrows = len(grid)
    ncols = len(grid[0])

    # load E, x, y, z
    with open(xyz_file) as f:
        counter = 1

        for p in p_rows:
            # in lieu of a loading screen
            if counter % 10 == 0:
                print(counter)

            # skip the first trajectory line where veclen == 0
            _ = f.readline()
            curr = f.readline().split(',')

            for j in range(2, p):
                nxt = f.readline().split(',')

                e, xi, yi, zi = [float(curr[i]) for i in range(2, 6)]
                _, xf, yf, zf = [float(nxt[i]) for i in range(2, 6)]

                # w : distance perpendicular to x
                wi = (yi**2 + zi**2)**0.5
                wf = (yf**2 + zf**2)**0.5
                dwdx = (wf - wi) / (xf - xi)

                ### horizontal entry
                if xf > xi:
                    grid_x_lo = np.ceil(xi / grid_sz)
                    grid_x_hi = np.floor(xf / grid_sz)
                elif xf < xi:
                    grid_x_hi = np.floor(xi / grid_sz)
                    grid_x_lo = np.ceil(xf / grid_sz)

                # horizontal direction cosine
                veclen = ((xf - xi)**2 + (yf - yi)**2 + (zf - zi)**2)**0.5
                alpha = (xf - xi) / veclen
                ang_x = float(np.arccos(abs(alpha)))

                for grid_x in range(int(grid_x_lo), int(grid_x_hi) + 1):
                    w = wi + (grid_x * grid_sz - xi) * dwdx
                    grid_w = int(np.floor(w / grid_sz))

                    if grid_x < nrows and grid_w < ncols:
                        grid[grid_x][grid_w]['num_ions'] += 1
                        grid[grid_x][grid_w]['energies'].append(e)
                        grid[grid_x][grid_w]['angles'].append(ang_x)

                curr = nxt

            counter += 1

    return grid

def print_grid(grid, prop):
    for row in grid:
        for col in row:
            print(f'{col[prop]}', end='; ')
        print()

def main():
    file_root = sys.argv[1]
    traj_row_file = file_root + '_trajectory_data.output'
    traj_xyz_file = file_root + '_trajectories.output'
    save_file = file_root + '_surface_grid.output'

    empty_grid = make_grid(90, 50)
    filled_grid = extract_from_traj(traj_row_file, traj_xyz_file, empty_grid, 1e3)
    print_grid(filled_grid, 'num_ions')

    with open(save_file, 'wb') as f:
        pickle.dump(filled_grid, f)

if __name__ == '__main__':
    main()
