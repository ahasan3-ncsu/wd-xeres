import sys
import numpy as np
from vispy import app, scene
from vispy.visuals.transforms import STTransform

from colors import custom_colors
from toml_util import get_sphere_prop, get_cube_prop

def create_vis(row_file, xyz_file, toml_file):
    jar = np.loadtxt(xyz_file, delimiter=',')

    Z = jar[:, 1]
    pos = jar[:, 3:6]

    canvas = scene.SceneCanvas(keys='interactive', bgcolor='w', show=True)
    view = canvas.central_widget.add_view()
    view.camera = 'turntable'

    z_colors = [custom_colors.get(z, (0.5, 0.5, 0.5, 1)) for z in Z]

    p_rows = np.loadtxt(row_file, dtype=int)
    line_sw = np.full(len(pos)-1, True)
    cum = 0
    for r in p_rows[:-1]:
        cum += r
        line_sw[cum-1] = False

    lines = scene.visuals.Line(
        pos=pos,
        color=z_colors,
        connect=line_sw,
        parent=view.scene
    )

    sphere_radius = get_sphere_prop(toml_file)
    sphere = scene.visuals.Sphere(
        radius=sphere_radius,
        method='latitude',
        color=(0.5, 0.5, 0.8, 0.3),
        parent=view.scene
    )

    cube_dim, cube_trf = get_cube_prop(toml_file)
    cube = scene.visuals.Box(
        *cube_dim,
        color=(0.8, 0.8, 0.8, 0.2),
        parent=view.scene
    )
    cube.transform = STTransform(translate=cube_trf)

    axis = scene.visuals.XYZAxis(parent=view.scene)

def main():
    file_root = sys.argv[1]
    traj_row_file = file_root + '_trajectory_data.output'
    traj_xyz_file = file_root + '_trajectories.output'
    toml_file = file_root + '.toml'

    create_vis(traj_row_file, traj_xyz_file, toml_file)
    app.run()

if __name__ == '__main__':
    main()
