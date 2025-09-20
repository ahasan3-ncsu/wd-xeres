import sys
import numpy as np
from vispy import app, scene
from vispy.visuals.transforms import STTransform

from colors import custom_colors
from toml_util import get_sphere_prop, get_cube_prop

def create_vis(disp_file, toml_file):
    jar = np.loadtxt(disp_file, delimiter=',')

    Z = jar[:, 1]
    pos_fin = jar[:, 6:9]

    canvas = scene.SceneCanvas(keys='interactive', show=True)
    view = canvas.central_widget.add_view()
    view.camera = 'turntable'

    z_colors = [custom_colors.get(z, (0.5, 0.5, 0.5, 1)) for z in Z]

    scatter = scene.visuals.Markers()
    scatter.set_data(pos_fin, edge_width=0, face_color=z_colors, size=5)
    view.add(scatter)

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
    disp_file = file_root + '_displacements.output'
    toml_file = file_root + '.toml'

    create_vis(disp_file, toml_file)
    app.run()

if __name__ == '__main__':
    main()
