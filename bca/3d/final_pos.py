import sys
import numpy as np
from vispy import app, scene, color

# feed a "displacements.output" file
fileName = sys.argv[1]
jar = np.loadtxt(fileName, delimiter=',')

Z = jar[:, 1]
Z_min, Z_max = np.min(Z), np.max(Z)
Z_norm = (Z - Z_min) / (Z_max - Z_min + 1e-8)

pos_ori = jar[:, 3:6]
pos_fin = jar[:, 6:9]

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'turntable'

cmap = color.colormap.get_colormap('autumn')
z_colors = cmap.map(Z_norm)

scatter = scene.visuals.Markers()
scatter.set_data(pos_fin, edge_width=0, face_color=z_colors, size=5)
view.add(scatter)

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

if __name__ == '__main__':
    app.run()
