import sys
import pickle
import numpy as np

def make_grid(rows, cols):
    grid = [
        [
            {
                'surf_area': 0.0,
                'num_ions': 0,
                'energies': [],
                'angles': []
            }
            for _ in range(cols)
        ]
        for _ in range(rows)
    ]

    for i in range(rows):
        for j in range(cols):
            rlo, rhi = max(0, j - 0.5), j + 0.5
            grid[i][j]['surf_area'] = np.pi * (rhi**2 - rlo**2)

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

                veclen = ((xf - xi)**2 + (yf - yi)**2 + (zf - zi)**2)**0.5
                if veclen == 0:
                    continue
                alpha = (xf - xi) / veclen
                if alpha < 0: # need to fix this later
                    print('Oops! Wrong direction.')
                    break
                ang = float(np.arccos(alpha))

                dydx = (yf - yi) / (xf - xi)
                dzdx = (zf - zi) / (xf - xi)

                gxi = np.ceil(xi / 1e3)
                gxf = np.floor(xf / 1e3)

                # print(xi, gxi, gxf, xf)
                # if gxi > gxf:
                #     break
                #     print(gxi, gxf)
                #     print('we are not cooked')

                # floor(x) = x is not considered; fix it later
                for gx in range(int(gxi), int(gxf) + 1):
                    gy = yi + (gx * 1e3 - xi) * dydx
                    gz = zi + (gx * 1e3 - xi) * dzdx

                    dd = (gy**2 + gz**2)**0.5
                    off = int(np.round(dd / 1e3))

                    # print(xi, xf)
                    # print(yi, yf, zi, zf)
                    # print(gy, gz)
                    # print(off)

                    grid[gx][off]['num_ions'] += 1
                    grid[gx][off]['energies'].append(e)
                    grid[gx][off]['angles'].append(ang)

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

    empty_grid = make_grid(90, 30)
    filled_grid = extract_from_traj(traj_row_file, traj_xyz_file, empty_grid)
    print_grid(filled_grid, 'num_ions')

    with open(save_file, 'wb') as f:
        pickle.dump(filled_grid, f)

if __name__ == '__main__':
    main()
