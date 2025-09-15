import numpy as np

jar = np.loadtxt('umo_0D_energy_loss.output', delimiter=',')

E_nuke = jar[:, 2]
E_elec = jar[:, 3]

nuke = E_nuke.sum()
elec = E_elec.sum()

print('Nuke: ', nuke)
print('Elec: ', elec)

print('Ratio: ', nuke / elec)
print('Total: ', nuke + elec)

# Outputs:
# Nuke:  488381050.6223347
# Elec:  9641618908.997154
# Ratio:  0.050653428146449346
# Total:  10129999959.61949
