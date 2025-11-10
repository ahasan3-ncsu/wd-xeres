import sys
import json

def calc(json_file):
    with open(json_file, 'r') as f:
        jar = json.load(f)

    num_ions = jar['num_ions']
    nuke = jar['nuke']
    elec = jar['elec']

    nuke_loss = sum(nuke) / num_ions
    elec_loss = sum(elec) / num_ions
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
