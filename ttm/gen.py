## Constants
gamma = 4e-9
# C_e is not constant anymore
#C_e = gamma * 400
rho_e = 0.625 # electrons/angstrom^3 (electronic_density)
esheat_0 = 0
esheat_1 = 0.000004
esheat_2 = 0
esheat_3 = 0
esheat_4 = 0
C_limit = 0

## Specific heat as a function of temperature
def el_sp_heat_integral(T_e):
    T_temp = T_e/1000.0
    return rho_e * (
        (esheat_0 + C_limit)*T_e         \
    	+ esheat_1*T_temp*T_e/2.0        \
    	+ esheat_2*T_temp*T_temp*T_e/3.0 \
    	+ esheat_3*pow(T_temp,3)*T_e/4.0 \
    	+ esheat_4*pow(T_temp,4)*T_e/5.0 \
    )

## Supercell setup
lat = 3.43
Lx = 20 * lat
Ly = 20 * lat
Lz = 20 * lat
R = 10 * lat

# Keep N even
Nx = 20; xMid = (Nx+1)/2
Ny = 20; yMid = (Ny+1)/2
Nz =  1 # thermal spike axis

# Cell dimensions
xCell = Lx/Nx
yCell = Ly/Ny
zCell = Lz/Nz

volCell = xCell * yCell * zCell
# rho_e is now in el_sp_heat_integral
#NeCell = rho_e * volCell

## Compute temperature in the grids
## and keep track of energy deposition
deposition = 0
def paw(i, j, k):
    ai = (i - xMid) * xCell
    aj = (j - yMid) * yCell
    r = (ai**2 + aj**2) ** 0.5

    ext_temp = 0
    if r <= R:
        ext_temp = 38e3 * (2.718281828)**(-(r/R)**2)

    # Relaxed temperature is 400 K
    T_e = 400 + ext_temp

    # global is needed because it's a function, not a loop
    global deposition
    deposition += el_sp_heat_integral(T_e) * volCell

    return T_e

# Write in a LAMMPS readable file
with open('Te.in', 'w') as f:
    f.write('# UNITS: metal COMMENT: initial electron temperature\n')

    for i in range(1, Nx+1):
        for j in range(1, Ny+1):
            for k in range(1, Nz+1):
                f.write(f'{i} {j} {k} {paw(i, j, k)}\n')

# Energy deposition along thermal spike axis
print('keV/nm: ', (deposition/Lz) / 1e2)
