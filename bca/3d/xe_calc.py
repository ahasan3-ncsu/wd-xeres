import matplotlib.pyplot as plt

E = []
R = []

with open('ballbox_displacements.output', 'r') as f:
    for line in f:
        tmp = line.split(',')
        if int(tmp[1]) == 54:
            E.append(float(tmp[2]))
            r2 = float(tmp[6])**2 + float(tmp[7])**2 + float(tmp[8])**2
            R.append(r2**0.5)

sorted_pair = sorted(zip(E, R))
E_sorted, R_sorted = zip(*sorted_pair)

print(
    ' Total Xe recoils: ', len(R_sorted), '\n',
    'Outside the sphere: ', sum(1 for x in R_sorted if x > 40), '\n',
    'Re-solved Xe: ', sum(1 for x in R_sorted if x > 50)
)

plt.scatter(E_sorted, R_sorted, marker='^', s=5)
plt.hlines(40, xmin=0, xmax=1000, color='r', label=r'$R_b$')
plt.hlines(50, xmin=0, xmax=1000, color='k', ls='--', label=r'$R_b + 10$')

plt.xscale('log')

plt.xlabel('Xe recoil energy (eV)')
plt.ylabel(r'Distance from the bubble center ($\AA$)')

plt.legend()
plt.show()
