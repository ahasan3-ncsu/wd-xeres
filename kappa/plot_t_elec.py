import matplotlib.pyplot as plt

def prn(fileName):
    with open(fileName, 'r') as f:
        jar = f.readlines()

    nx = []
    temp = []

    for line in jar[2:]:
        tmp = line.split()
        nx.append(float(tmp[0]))
        temp.append(float(tmp[3]))

    tstep = fileName.split('.')[2]
    plt.plot(nx, temp, label=f'step: {tstep}')

for t in range(2500000, 4000001, 500000):
    prn(f'run9_250_grids/elec_temp.out.{t}')

plt.xlabel('Grid number')
plt.ylabel('Temperature (K)')
#plt.ylim([1080, 1320])

plt.legend()
plt.show()
