import sys
from toml_util import get_sphere_prop

def calc(disp_file, toml_file):
    R_ini = []
    R_fin = []

    with open(disp_file, 'r') as f:
        for line in f:
            if line[:6] == '134,54':
                tmp = line.split(',')

                r2 = float(tmp[3])**2 + float(tmp[4])**2 + float(tmp[5])**2
                R_ini.append(r2**0.5)
                r2 = float(tmp[6])**2 + float(tmp[7])**2 + float(tmp[8])**2
                R_fin.append(r2**0.5)

    Rb = get_sphere_prop(toml_file)
    L = 10

    print(
        ' Total Xe recoils: ', len(R_fin), '\n',
        'Outside the sphere: ', sum(1 for x in R_fin if x > Rb), '\n',
        'Re-solved Xe: ', sum(1 for x in R_fin if x > (Rb + L))
    )

def main():
    file_root = sys.argv[1]
    disp_file = file_root + '_displacements.output'
    toml_file = file_root + '.toml'

    calc(disp_file, toml_file)

if __name__ == '__main__':
    main()
