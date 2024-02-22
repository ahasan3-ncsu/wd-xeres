import matplotlib.pyplot as plt

with open('spikeavg.30ang30keVpnm_long') as f:
    l = f.readlines()

l = l[2:]
l_time = []
l_temp = []
for line in l:
    tmp = line.split()
    l_time.append(float(tmp[2]))
    l_temp.append(float(tmp[3]))

with open('spikeavg.30ang30keVpnm_short') as f:
    s = f.readlines()

s = s[2:]
s_time = []
s_temp = []
for line in s:
    tmp = line.split()
    s_time.append(float(tmp[2]))
    s_temp.append(float(tmp[3]))

plt.figure(figsize=(5,4))

plt.plot(l_time, l_temp, label='long run')
plt.plot(s_time, s_temp, label='short run')
plt.hlines(y=500, xmin=100, xmax=1720,
           ls='dashed', colors='black', label='T=500 K')
plt.hlines(y=800, xmin=100, xmax=1720,
           ls='dotted', colors='black', label='T=800 K')

plt.xlabel('Time (ps)')
plt.ylabel('Temperature (K)')

plt.legend()
plt.tight_layout()
plt.savefig('comparison.jpg', dpi=300)
