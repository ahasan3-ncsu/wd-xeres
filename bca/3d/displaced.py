import numpy as np
from vispy import app, scene, color

jar = np.loadtxt('ballbox_displacements.output', delimiter=',')

Z = jar[:, 1]
Z_min, Z_max = np.min(Z), np.max(Z)
Z_norm = (Z - Z_min) / (Z_max - Z_min + 1e-8)

pos_ori = jar[:, 3:6]
pos_fin = jar[:, 6:9]

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'turntable'

v1 = np.empty((2 * pos_ori.shape[0], 3))
v1[0::2] = pos_ori
v1[1::2] = pos_fin
v2 = np.hstack((pos_ori, pos_fin))

cmap = color.colormap.get_colormap('autumn')
arrow_colors = cmap.map(Z_norm)
arrow_colors_repeated = np.repeat(arrow_colors, 2, axis=0)

arrow = scene.visuals.Arrow(
    v1,
    arrows=v2,
    arrow_size=3,
    connect='segments',
    color=arrow_colors_repeated,
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

if __name__ == '__main__':
    app.run()
