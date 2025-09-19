import sys
import numpy as np
from vispy import app, scene

# feed a "displacements.output" file
fileName = sys.argv[1]
jar = np.loadtxt(fileName, delimiter=',')

Z = jar[:, 1]
pos_ori = jar[:, 3:6]
pos_fin = jar[:, 6:9]

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'turntable'

v1 = np.empty((2 * pos_ori.shape[0], 3))
v1[0::2] = pos_ori
v1[1::2] = pos_fin
v2 = np.hstack((pos_ori, pos_fin))

custom_colors = {
    39: (0.0, 1.0, 1.0, 1), # Y  = Cyan
    42: (0.0, 0.0, 1.0, 1), # Mo = Blue
    53: (0.0, 1.0, 0.0, 1), # I  = Green
    54: (1.0, 1.0, 0.0, 1), # Xe = Yellow
    92: (1.0, 0.0, 0.0, 1)  # U  = Red
}
line_colors = [custom_colors.get(z, (0.5, 0.5, 0.5, 1)) for z in Z]
line_colors_repeated = np.repeat(line_colors, 2, axis=0)

arrow = scene.visuals.Arrow(
    pos=v1,
    color=line_colors_repeated,
    connect='segments',
    arrows=v2,
    arrow_size=3,
    parent=view.scene
)

sphere = scene.visuals.Sphere(
    radius=40,
    method='latitude',
    color=(0.5, 0.5, 0.8, 0.3),
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
