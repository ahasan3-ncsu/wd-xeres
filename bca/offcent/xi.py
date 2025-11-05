import sys
import json
import pickle
import numpy as np
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm

def extract_grid(grid_file):
    with open(grid_file, 'rb') as f:
        grid_data = pickle.load(f)

    return grid_data

def add_prob(grid_data, grid_info):
    cell_size, num_rows, num_cols = (
        grid_info['cell_size'], grid_info['num_rows'], grid_info['num_cols']
    )

    total_ions = grid_data[0][0]['num_ions']
    for i in range(num_rows):
        for j in range(num_cols):
            surf_area = np.pi * ((j+1)**2 - j**2) * cell_size**2
            grid_data[i][j]['probability'] = (
                grid_data[i][j]['num_ions'] / total_ions / surf_area
            )

    return grid_data

def pchip_splines(json_file):
    with open(json_file, 'r') as f:
        jar = json.load(f)

    L = jar['L']
    E = jar['E']
    chi = jar['chi']

    splines = []
    for i in range(len(L)):
        # E -> MeV; chi[i] -> fraction
        splines.append(PchipInterpolator(E, chi[i]))

    return L, splines

def get_chi(L, splines, energy, l):
    # convert to MeV
    en_mev = energy / 1e6

    Lchi = []
    for spl in splines:
        Lchi.append(max(0, spl(en_mev)))

    # lspline = PchipInterpolator(L, Lchi)
    # return lspline(l)
    return np.interp(l, L, Lchi)

def get_grid_points(x, w, alpha, D, hi, lo, T):
    cos_a = np.cos(alpha)
    sin_a = np.sin(alpha)

    xp, wp = x  - D  * cos_a, w  - D  * sin_a
    p1, q1 = xp - hi * sin_a, wp + hi * cos_a
    p2, q2 = xp + hi * sin_a, wp - hi * cos_a
    f1, f2 = (hi - lo) / (2 * hi), (hi + lo) / (2 * hi)

    points = []
    for t1 in T:
        p = p1 + t1 * (p2 - p1)
        q = q1 + t1 * (q2 - q1)
        for t2 in T:
            # discard points outside the region
            if f1 < t1 and t1 < f2 and f1 < t2 and t2 < f2:
                continue

            z = -hi + t2 * (2 * hi)
            # point in question: (p, q, z)
            # central point: (xp, wp, 0)
            _w = (q**2 + z**2) ** 0.5
            _l = ((p - xp)**2 + (q - wp)**2 + z**2) ** 0.5
            points.append((p, _w, _l))

    return points

def add_xi(grid_data, grid_info, L, splines, mesh_info):
    cell_size, num_rows, num_cols = (
        grid_info['cell_size'], grid_info['num_rows'], grid_info['num_cols']
    )

    Rb, delta, n_regions, reg_bounds, reg_divs = (
        mesh_info['Rb'], mesh_info['delta'],
        mesh_info['n_regions'], mesh_info['reg_bounds'], mesh_info['reg_divs']
    )
    assert len(reg_bounds) == (n_regions + 1)
    assert len(reg_divs) == n_regions

    D = Rb + delta

    for r in range(n_regions):
        hi, lo = reg_bounds[r], reg_bounds[r+1]
        s = 2 * hi / reg_divs[r]
        k = 2 * lo / s
        assert abs(round(k) * s - 2 * lo) < 1e-6

    bigT = []
    for divs in reg_divs:
        T = np.linspace(0, 1, divs+1)
        T = (T[1:] + T[:-1]) / 2
        bigT.append(T)

    for i in range(num_rows):
        for j in range(num_cols):
            # no ion in these cells
            if not grid_data[i][j]['num_ions']:
                grid_data[i][j]['xi'] = 0
                continue

            x, w = i * cell_size, j * cell_size
            alpha = grid_data[i][j]['angles']
            cos_a = np.cos(alpha)

            sum = 0.0

            for r in range(n_regions):
                hi, lo = reg_bounds[r], reg_bounds[r+1]
                s = 2 * hi / reg_divs[r]

                reg_sum = 0.0

                points = get_grid_points(x, w, alpha, D, hi, lo, bigT[r])
                for p in points:
                    xp, wp, lp = p
                    ip = np.clip(int(xp / cell_size), 0, num_rows - 1)
                    jp = np.clip(int(wp / cell_size), 0, num_cols - 1)
                    # better corner case impl. needed
                    # for now, remove elements with notably different angles
                    if abs(grid_data[ip][jp]['angles'] - alpha) > 0.8:
                        continue

                    reg_sum += (
                        grid_data[ip][jp]['probability']
                        * get_chi(
                                L, splines,
                                grid_data[ip][jp]['energies'], lp
                            )
                    )

                reg_sum *= s**2 / cos_a

                sum += reg_sum

            grid_data[i][j]['xi'] = sum

    # ff origin cannot be inside the bubble
    for i in range(Rb // cell_size + 1):
        grid_data[i][0]['xi'] = 0

    return grid_data

def add_db(grid_data, grid_info):
    cell_size, num_rows, num_cols = (
        grid_info['cell_size'], grid_info['num_rows'], grid_info['num_cols']
    )

    b = 0.0
    for i in range(num_rows):
        for j in range(num_cols):
            surf_area = np.pi * ((j+1)**2 - j**2) * cell_size**2
            grid_data[i][j]['db'] = (
                grid_data[i][j]['xi']
                * surf_area * cell_size
            )
            b += grid_data[i][j]['db']

    print(b * 1e-30) # b/Fdot; angstrom^3 -> m^3
    return grid_data

def plot_prop(grid_data, prop, pnorm):
    prop_data = [
        [col[prop] for col in row]
        for row in grid_data
    ]
    t_data = np.array(prop_data).T

    plt.imshow(t_data,
               cmap='nipy_spectral',
               origin='lower',
               norm=pnorm)
    plt.colorbar()
    plt.show()

def get_mesh_regions(Rb, delta):
    hi = Rb + delta
    outer_res = 500 / 2**0.5
    inner_res = min(Rb / 2, outer_res)
    cutoff = 2 * Rb

    n_regs = 0
    bounds = [hi]
    divs = []

    while hi > cutoff:
        # ensure at most outer_res
        div = 3
        while (2 * hi / div) > outer_res:
            div += 1

        # slowly go down to inner_res if current res doesn't work
        k = 0
        while (2 * hi / div) > inner_res:
            s = 2 * hi / div

            k = 0
            while (hi - k * s) >= cutoff:
                k += 1
            k -= 1

            if k > 0:
                break
            else:
                div += 1

        if k > 0:
            n_regs += 1
            lo = hi - k * s
            bounds.append(lo)
            divs.append(div)
            hi = lo
        else:
            # time to switch to inner region
            break

    # inner region
    n_regs += 1
    bounds.append(0)
    divs.append(int(np.ceil(2 * hi / inner_res)))

    return n_regs, bounds, divs

def main():
    rad = sys.argv[1]
    ion = sys.argv[2]

    json_file = f'data/{rad}nm_{ion}.json'
    grid_file = f'data/{ion}_surface_grid.output'

    print(json_file)
    print(grid_file)

    # ANGSTROM
    grid_info = {
        'cell_size': 500,
        'num_rows' : 180,
        'num_cols' : 100,
    }

    Rb = int(rad) * 10
    delta = 1000
    n_regs, bounds, divs = get_mesh_regions(Rb, delta)
    print(f'{n_regs}\n{bounds}\n{divs}\n')

    mesh_info = {
        'Rb'        : Rb,
        'delta'     : delta,
        'n_regions' : n_regs,
        'reg_bounds': bounds,
        'reg_divs'  : divs,
    }

    L, splines = pchip_splines(json_file)

    grid = extract_grid(grid_file)
    grid = add_prob(grid, grid_info)
    grid = add_xi(grid, grid_info, L, splines, mesh_info)
    grid = add_db(grid, grid_info)

    # plot_prop(grid, 'probability', SymLogNorm(linthresh=1e-11))
    # plot_prop(grid, 'energies', 'linear')

    # plot_prop(grid, 'xi', SymLogNorm(linthresh=1e-12))
    # plot_prop(grid, 'db', SymLogNorm(linthresh=1e-2))

if __name__ == '__main__':
    main()
