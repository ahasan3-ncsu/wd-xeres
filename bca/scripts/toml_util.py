import tomllib

def get_sphere_prop(toml_file):
    with open(toml_file, 'rb') as f:
        jar = tomllib.load(f)

    return jar['geometry_input'].get('sphere_radius', 1e3)

def get_cube_prop(toml_file):
    with open(toml_file, 'rb') as f:
        jar = tomllib.load(f)

    lo, hi = jar['geometry_input'].get(
        'cuboid_corners', [[0, -3e4, -3e4], [9e4, 3e4, 3e4]]
    )
    dim = [hi[i] - lo[i] for i in range(3)]
    trf = [(lo[i] + hi[i]) / 2 for i in range(3)]

    return dim, trf
