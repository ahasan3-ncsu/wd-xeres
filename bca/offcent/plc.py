import os
import json
import matplotlib.pyplot as plt

def main():
    data_dir = 'data'
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    print(json_files)

    for jname in json_files:
        jpath = os.path.join(data_dir, jname)
        with open(jpath, 'r') as f:
            foo = json.load(f)

        L = foo['L']
        chi = foo['chi']

        # normalize
        L = [l / L[-1] for l in L]
        chi = [c / chi[0] for c in chi]

        plt.plot(L, chi, label=f'{jname[:-5]}')

    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
