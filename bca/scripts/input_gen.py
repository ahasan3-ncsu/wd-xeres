import sys
import tomlkit

def read_toml(toml_file):
    with open('ballbox.toml', 'r') as f:
        data = tomlkit.load(f)

    dir = data['particle_parameters']['dir'][0]
    print(dir[0]**2 + dir[1]**2)
    print(data['geometry_input']['sphere_radius'])
    print(data['geometry_input']['cuboid_corners'])

def main():
    toml_file = sys.argv[1]

    read_toml(toml_file)

if __name__ == '__main__':
    main()
