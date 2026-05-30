import sys
import json
import numpy as np

def calc(json_file):
    with open(json_file, 'r') as f:
        jar = json.load(f)

    num_ions = np.sum(jar['num_ions'])
    nuke_all = np.sum(jar['nuke'])
    elec_all = np.sum(jar['elec'])

    # *_loss is a per ion quantity
    nuke_loss = nuke_all / num_ions
    elec_loss = elec_all / num_ions
    total_loss = nuke_loss + elec_loss

    print('nuke_loss: ', nuke_loss)
    print('elec_loss: ', elec_loss)

    print('Total: ', total_loss)
    print('Nuke ratio: ', nuke_loss / total_loss)
    print('Elec ratio: ', elec_loss / total_loss)

def main():
    file_root = sys.argv[1]
    json_file = file_root + '_eloss_bin.json'
    print(json_file)

    calc(json_file)

if __name__ == '__main__':
    main()
