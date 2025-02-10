gamma = 4e-9
C_e = gamma * 400
rho_e = 0.625 # electrons/angstrom^3

lat = 3.43
Lx = 20 * lat
Ly = 20 * lat
Lz = 20 * lat
R = 10 * lat
#R = 15

# Keep N even.
Nx = 20; xMid = (Nx+1)/2
Ny = 20; yMid = (Ny+1)/2
Nz =  1

xCell = Lx/Nx
yCell = Ly/Ny
zCell = Lz/Nz

volCell = xCell * yCell * zCell
NeCell = rho_e * volCell

deposition = 0
def paw(i, j, k):
    ai = (i - xMid) * xCell
    aj = (j - yMid) * yCell
    r = (ai**2 + aj**2) ** 0.5

    ext_temp = 0
    if r <= R:
        ext_temp = 32e3 * (2.718281828)**(-(r/R)**2)

    T_e = 400 + ext_temp

    global deposition
    deposition += T_e * C_e * NeCell

    return T_e

with open('Te.in', 'w') as f:
    f.write('# UNITS: metal COMMENT: initial electron temperature\n')

    for i in range(1, Nx+1):
        for j in range(1, Ny+1):
            for k in range(1, Nz+1):
                f.write(f'{i} {j} {k} {paw(i, j, k)}\n')

print('WRONG keV/nm: ', (deposition/Lz) / 1e2)
