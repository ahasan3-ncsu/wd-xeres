import sys
import pickle
import numpy as np

from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED

def make_grid(rows, cols, sz):
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
            # sz^2 is there to make it angstrom^2
            grid[i][j]['surf_area'] = np.pi * ((j+1)**2 - j**2) * sz**2

    return grid

def chunk_stream(row_file, xyz_file):
    p_rows = np.loadtxt(row_file, dtype=int)

    with open(xyz_file) as f:
        for p in p_rows:
            jar = []
            for _ in range(p):
                jar.append(f.readline())

            yield jar

def process_chunk(data, nrows, ncols, grid_sz):
    foo = {}

    # skip the first trajectory line where veclen == 0
    curr = data[1].split(',')

    for j in range(2, len(data)):
        nxt = data[j].split(',')

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
                if (grid_x, grid_w) in foo:
                    foo[(grid_x, grid_w)][0] += 1
                    foo[(grid_x, grid_w)][1].append(e)
                    foo[(grid_x, grid_w)][2].append(ang_x)
                else:
                    foo[(grid_x, grid_w)] = [1, [e], [ang_x]]

        curr = nxt

    return foo

def aggregate(grid, increments):
    for incr in increments:
        for k, v in incr.items():
            grid[k[0]][k[1]]['num_ions'] += v[0]
            grid[k[0]][k[1]]['energies'].extend(v[1])
            grid[k[0]][k[1]]['angles'].extend(v[2])

    return grid

def extract_from_traj(row_file, xyz_file, grid, grid_sz):
    # number of rows for ions
    p_rows = np.loadtxt(row_file, dtype=int)
    gen = chunk_stream(row_file, xyz_file)

    nrows = len(grid)
    ncols = len(grid[0])

    increments = []

    workers = max(1, cpu_count() - 2)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = set()

        counter = 1
        for _ in p_rows:
            # in lieu of a loading screen
            if counter % 10 == 0:
                print(f'Submitted {counter} chunks')

            jar = next(gen)

            future = executor.submit(process_chunk, jar, nrows, ncols, grid_sz)
            futures.add(future)

            if len(futures) >= workers:
                done, futures = wait(futures, return_when=FIRST_COMPLETED)
                for d in done:
                    increments.append(d.result())

            counter += 1

        for future in futures:
            increments.append(future.result())

    return aggregate(grid, increments)

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

    grid_size = int(5e2) # 50 nm should be enough
    num_rows = int(9e4 / grid_size) # 9 micron in width
    num_cols = int(5e4 / grid_size) # 5 micron in height
    print(f'{num_rows}x{num_cols} grids of size {grid_size} angstrom')

    empty_grid = make_grid(num_rows, num_cols, grid_size)
    filled_grid = extract_from_traj(
        traj_row_file, traj_xyz_file, empty_grid, grid_size
    )
    # print_grid(filled_grid, 'num_ions')

    with open(save_file, 'wb') as f:
        pickle.dump(filled_grid, f)

if __name__ == '__main__':
    main()
