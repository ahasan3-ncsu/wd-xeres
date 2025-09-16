import numpy as np
import matplotlib.pyplot as plt

jar = np.loadtxt('umo_0D_energy_loss.output', delimiter=',')

x = jar[:, 4]
E_nuke = jar[:, 2]

del jar

bin_width = 5000
x_min, x_max = x.min(), x.max()

bins = np.arange(x_min, x_max + bin_width, bin_width)
bin_centers = (bins[:-1] + bins[1:]) / 2

x_bin = np.digitize(x, bins)

nuke_loss_per_bin = np.zeros(len(bins) - 1)

np.add.at(nuke_loss_per_bin, x_bin - 1, E_nuke)
cum_nuke_loss = np.cumsum(nuke_loss_per_bin)

plt.figure(figsize=(5, 4))

plt.plot(
    bin_centers / 1e4,
    nuke_loss_per_bin / 1e8,
    label='Local',
    marker='o',
    markersize=3,
    color='red'
)
plt.plot(
    bin_centers / 1e4,
    cum_nuke_loss / 1e8,
    label='Cumulative',
    marker='s',
    markersize=3,
    ls='-.',
    color='peru'
)

plt.title(r'$^{97}_{39}Y$, 101.3 MeV')
# plt.title(r'$^{136}_{53}I$, 74.6 MeV')
plt.xlabel(r'Distance ($\mu$m)')
plt.ylabel(r'Nuclear energy loss (MeV)')

plt.legend()
plt.savefig('nuke_loss.pdf')
