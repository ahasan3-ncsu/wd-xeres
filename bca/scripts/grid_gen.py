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
                'angles': []       # radian (0 -> pi)
            }
            for _ in range(cols)
        ]
        for _ in range(rows)
    ]

    for i in range(rows):
        for j in range(cols):
            rlo, rhi = max(0, j - 0.5), j + 0.5
            # 1e6 is there to make it angstrom^2
            grid[i][j]['surf_area'] = np.pi * (rhi**2 - rlo**2) * 1e6

    return grid

def extract_from_traj(row_file, xyz_file, grid):
    # number of rows for ions
    p_rows = np.loadtxt(row_file, dtype=int)

    # load E, x, y, z
    with open(xyz_file) as f:
        for k in p_rows:
            jar = []
            for i in range(k):
                tmp = f.readline().split(',')
                jar.append([float(tmp[i]) for i in range(2, 6)])

            for j in range(1, len(jar)):
                e, xi, yi, zi = jar[j-1]
                _, xf, yf, zf = jar[j]

                # corner case: sometimes position doesn't change
                veclen = ((xf - xi)**2 + (yf - yi)**2 + (zf - zi)**2)**0.5
                if veclen == 0:
                    continue

                # slopes
                dydx = (yf - yi) / (xf - xi)
                dzdx = (zf - zi) / (xf - xi)

                # direction cosine
                alpha = (xf - xi) / veclen

                if alpha > 0:
                    ang = float(np.arccos(alpha))

                    grid_lo = np.ceil(xi / 1e3)
                    # strict floor not needed; x == floor(x) is unlikely
                    grid_hi = np.floor(xf / 1e3)
                elif alpha < 0:
                    ang = float(np.arccos(-alpha))

                    grid_hi = np.floor(xi / 1e3)
                    # strict ceil not needed; x == ceil(x) is unlikely
                    grid_lo = np.ceil(xf / 1e3)

                for grid_x in range(int(grid_lo), int(grid_hi) + 1):
                    y = yi + (grid_x * 1e3 - xi) * dydx
                    z = zi + (grid_x * 1e3 - xi) * dzdx

                    r_yz = (y**2 + z**2)**0.5
                    grid_off = int(np.round(r_yz / 1e3))

                    grid[grid_x][grid_off]['num_ions'] += 1
                    grid[grid_x][grid_off]['energies'].append(e)
                    grid[grid_x][grid_off]['angles'].append(ang)

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
    save_file = file_root + '_grid_data.output'

    empty_grid = make_grid(90, 40)
    filled_grid = extract_from_traj(traj_row_file, traj_xyz_file, empty_grid)
    print_grid(filled_grid, 'num_ions')

    with open(save_file, 'wb') as f:
        pickle.dump(filled_grid, f)

if __name__ == '__main__':
    main()
