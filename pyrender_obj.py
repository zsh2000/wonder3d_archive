import numpy as np
import trimesh
import pyrender
import matplotlib.pyplot as plt


fuze_trimesh = trimesh.load('/home/zheng720/wonder3d/Wonder3D/instant-nsr-pl/exp/0_alpha/@20241108-125011/save/it3000-mc192.obj')
mesh = pyrender.Mesh.from_trimesh(fuze_trimesh)
scene = pyrender.Scene()
scene.add(mesh)
camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.0)
s = np.sqrt(2)/2
camera_pose = np.array([
   [1.0,  0,   0,   0],
   [0.0,  0.0, 1.0, -1.3],
   [0.0,  -1,   0,  0],
   [0.0,  0.0, 0.0, 1.0],
])
scene.add(camera, pose=camera_pose)
light = pyrender.SpotLight(color=np.ones(3), intensity=3.0,
                           innerConeAngle=np.pi/16.0,
                           outerConeAngle=np.pi/6.0)
scene.add(light, pose=camera_pose)
r = pyrender.OffscreenRenderer(1024, 1024)
color, depth = r.render(scene)

print(color.min())
# plt.figure()
# plt.subplot(1,2,1)
# plt.axis('off')
# plt.imshow(color)
# plt.subplot(1,2,2)
# plt.axis('off')
# plt.imshow(depth, cmap=plt.cm.gray_r)
# plt.show()
