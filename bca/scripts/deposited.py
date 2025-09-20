import sys
import numpy as np
from vispy import app, scene
from colors import custom_colors

# feed a "deposited.output" file
fileName = sys.argv[1]
jar = np.loadtxt(fileName, delimiter=',')

Z = jar[:, 1]
pos_fin = jar[:, 2:5]

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'turntable'

z_colors = [custom_colors.get(z, (0.5, 0.5, 0.5, 1)) for z in Z]

scatter = scene.visuals.Markers()
scatter.set_data(pos_fin, edge_width=0, face_color=z_colors, size=5)
view.add(scatter)

sphere = scene.visuals.Sphere(
    radius=1000,
    method='latitude',
    color=(0.8, 0.2, 0.2, 0.8),
    parent=view.scene
)

cube = scene.visuals.Box(
    10000, 10000, 10000,
    color=(0.8, 0.8, 0.8, 0.2),
    parent=view.scene
)

axis = scene.visuals.XYZAxis(parent=view.scene)

if __name__ == '__main__':
    app.run()
