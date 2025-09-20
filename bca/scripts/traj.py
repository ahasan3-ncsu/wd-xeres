import sys
import numpy as np
from vispy import app, scene

def create_vis(row_file, xyz_file):
    jar = np.loadtxt(xyz_file, delimiter=',')

    Z = jar[:, 1]
    pos = jar[:, 3:6]

    canvas = scene.SceneCanvas(keys='interactive', show=True)
    view = canvas.central_widget.add_view()
    view.camera = 'turntable'

    custom_colors = {
        39: (0.0, 1.0, 1.0, 1), # Y  = Cyan
        42: (0.0, 0.0, 1.0, 1), # Mo = Blue
        53: (0.0, 1.0, 0.0, 1), # I  = Green
        54: (1.0, 1.0, 0.0, 1), # Xe = Yellow
        92: (1.0, 0.0, 0.0, 1)  # U  = Red
    }
    z_colors = [custom_colors.get(z, (0.5, 0.5, 0.5, 1)) for z in Z]

    # It'd be perfect if it could be fully transparent.
    rows = np.loadtxt(row_file, dtype=int)
    rc = np.cumsum(rows)
    for i in rc:
        z_colors[i-1] = (0, 0, 0, 0)

    lines = scene.visuals.Line(
        pos=pos,
        color=z_colors,
        connect='strip',
        parent=view.scene
    )

    sphere = scene.visuals.Sphere(
        radius=40,
        method='latitude',
        color=(0.5, 0.5, 0.8, 0.2),
        parent=view.scene
    )

    cube = scene.visuals.Box(
        160, 160, 160,
        color=(0.8, 0.8, 0.8, 0.2),
        parent=view.scene
    )

    axis = scene.visuals.XYZAxis(parent=view.scene)

def main():
    file_root = sys.argv[1]
    traj_row_file = file_root + '_trajectory_data.output'
    traj_xyz_file = file_root + '_trajectories.output'

    create_vis(traj_row_file, traj_xyz_file)
    app.run()

if __name__ == '__main__':
    main()
