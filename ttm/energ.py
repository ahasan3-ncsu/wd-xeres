lat = 3.43
rho_e = 0.625 # electrons/angstrom^3
Lx = 160 * lat
Ly = 160 * lat
Lz = 6 * lat
# R = 10 * lat
R = 15

# electronic grid
Nx = 80; xMid = (Nx+1)/2
Ny = 80; yMid = (Ny+1)/2
Nz =  1

xCell = Lx/Nx
yCell = Ly/Ny
zCell = Lz/Nz

volCell = xCell * yCell * zCell
NeCell = rho_e * volCell

def exp(x):
    return (2.718281828)**(x)

def paw(i, j, k):
    ai = (i - xMid) * xCell
    aj = (j - yMid) * yCell
    r = (ai**2 + aj**2) ** 0.5

    if r > R:
        return 0
    else:
        pre = 80000
        temp = pre * exp(-(r/R)**2)
        print(i, j, k, temp)

        kePatom = 3/2 * 8.617e-5 * temp
        keCell = NeCell * kePatom
        return keCell

sum = 0
for i in range(1, Nx+1):
    for j in range(1, Ny+1):
        for k in range(1, Nz+1):
            sum += paw(i, j, k)

print('keV/nm: ', (sum/Lz) / 1e2) # deposition in keV/nm
