import sys
import matplotlib.pyplot as plt

files = sys.argv[1:]
print(files)

with open(files[0], 'r') as f:
    jar = f.readlines()

nChunk = 10
for i in range(4, 113, nChunk+1):
    x = []; y = []

    for k in range(i, i+10):
        tmp = jar[k].split()
        x.append(int(tmp[0]))
        y.append(float(tmp[1]))

    plt.plot(x, y, color=plt.cm.plasma( (1-i/223) ))

plt.xlabel('Distance from centerline (Ang)')
plt.ylabel('Temperature (K)')
plt.show()
