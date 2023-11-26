import matplotlib.pyplot as plt

with open('Srim_UMoXe.es', 'r') as f:
    jar = f.readlines()

jar = jar[3:]

x = []
U = []
Mo = []
Xe = []

for line in jar:
    tmp = line.split()
    x.append(float(tmp[0]))
    U.append(float(tmp[1]))
    Mo.append(float(tmp[2]))
    Xe.append(float(tmp[3]))

plt.plot(x, U, label='U')
plt.plot(x, Mo, label='Mo')
plt.plot(x, Xe, label='Xe')

plt.legend()
plt.show()
