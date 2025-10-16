import tomlkit
import argparse

def gen_toml(arg_dict):
    ### READ
    with open(arg_dict['filename'], 'r') as f:
        toml_dict = tomlkit.load(f)

    ### GEOMETRY
    delta = 1e3    # 0.1 micron separation
    radius = float(arg_dict['sphere'][0])
    density = float(arg_dict['sphere'][1])
    box_half = radius + delta + 1.0

    toml_dict['geometry_input']['sphere_radius'] = radius
    toml_dict['geometry_input']['sphere_densities'] = [0.0, 0.0, density]
    toml_dict['geometry_input']['cuboid_corners'] = [
        [-box_half, -box_half, -box_half], [box_half, box_half, box_half]
    ]

    ### YTTRIUM
    y_num = int(arg_dict['yttrium'][0])
    toml_dict['particle_parameters']['N'][0] = y_num

    y_en = float(arg_dict['yttrium'][1])
    toml_dict['particle_parameters']['E'][0] = y_en

    y_l = float(arg_dict['yttrium'][2])
    toml_dict['particle_parameters']['pos'][0] = [
        - radius - delta, y_l / 2**0.5, y_l / 2**0.5
    ]

    y_str = ''
    if y_num:
        y_str = f'_Y_{y_en/1e6:.1f}MeV'
        if y_l:
            y_str += f'_l{y_l/10:.0f}nm'

    ### IODINE
    i_num = int(arg_dict['iodine'][0])
    toml_dict['particle_parameters']['N'][1] = i_num

    i_en = float(arg_dict['iodine'][1])
    toml_dict['particle_parameters']['E'][1] = i_en

    i_l = float(arg_dict['iodine'][2])
    toml_dict['particle_parameters']['pos'][1] = [
        - radius - delta, i_l / 2**0.5, i_l / 2**0.5
    ]

    i_str = ''
    if i_num:
        i_str = f'_I_{i_en/1e6:.1f}MeV'
        if i_l:
            i_str += f'_l{i_l/10:.0f}nm'

    ### WRITE
    file_root = arg_dict['filename'].split('.')[0]
    output_name = file_root + f'_{radius/10:.0f}nm' + y_str + i_str
    toml_dict['options']['name'] = output_name + '_'

    output_toml = output_name + '.toml'
    with open(output_toml, 'w') as f:
        tomlkit.dump(toml_dict, f)

    return output_toml

def main():
    parser = argparse.ArgumentParser(
        prog='ballbox replicator',
        description='Generate a new input.toml based on ballbox',
        epilog='see you space cowboy'
    )

    parser.add_argument('filename', help='original ballbox.toml file')
    parser.add_argument(
        '-Y', '--yttrium',
        nargs=3,
        metavar=('N', 'E', 'l'),
        help='Y number, energy and off-centered distance',
    )
    parser.add_argument(
        '-I', '--iodine',
        nargs=3,
        metavar=('N', 'E', 'l'),
        help='I number, energy and off-centered distance'
    )
    parser.add_argument(
        '-S', '--sphere',
        nargs=2,
        metavar=('R', 'rho'),
        help='sphere radius and number density'
    )

    args = parser.parse_args()

    print(vars(args))
    print(gen_toml(vars(args)))

if __name__ == '__main__':
    main()
