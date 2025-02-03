import bpy
import mathutils

import math


# Enable the OBJ Import/Export add-on
if not bpy.ops.import_scene.obj.poll():
    bpy.ops.preferences.addon_enable(module="io_scene_obj")


# Clear the scene (delete all objects)
bpy.ops.wm.read_factory_settings(use_empty=True)

# Load the OBJ file
obj_path = "/home/zheng720/wonder3d/Wonder3D/instant-nsr-pl/exp/0_alpha/@20241108-125452/save/it3000-mc192.obj"
bpy.ops.import_scene.obj(filepath=obj_path)

## Define the RT matrix
## Rotation (example with 45 degrees around each axis)
#rot_x = mathutils.Matrix.Rotation(math.radians(45), 4, 'X')
#rot_y = mathutils.Matrix.Rotation(math.radians(30), 4, 'Y')
#rot_z = mathutils.Matrix.Rotation(math.radians(60), 4, 'Z')
#
## Combine rotations
#rotation_matrix = rot_x @ rot_y @ rot_z


# 1.000000000000000000e+00 0.000000000000000000e+00 0.000000000000000000e+00 0.000000000000000000e+00
# 0.000000000000000000e+00 -1.343588564850506373e-07 1.000000119209289551e+00 -1.746665105883948854e-07
# 0.000000000000000000e+00 -1.000000119209289551e+00 -1.343588564850506373e-07 -1.300000071525573730e+00


rotation_matrix = mathutils.Matrix(((1, 0, 0, 0), (0, 0, 1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))

# Translation (example translation vector)
translation = mathutils.Vector((0.0, 0.0, 0))

# Create a 4x4 matrix with the rotation and translation
RT_matrix = rotation_matrix.copy()
RT_matrix.translation = translation

# Set up an orthographic camera and apply the RT matrix
cam_data = bpy.data.cameras.new("Camera")
cam_data.type = 'ORTHO'  # Set camera to orthographic
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam

# Set the orthographic scale (controls zoom level)
cam.data.ortho_scale = 1.0  # adjust as needed

# Apply the RT matrix to the camera
cam.matrix_world = RT_matrix

# Set render resolution and file format
bpy.context.scene.render.resolution_x = 1024
bpy.context.scene.render.resolution_y = 1024
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Set output path
output_path = "./image_rendered_2.png"
bpy.context.scene.render.filepath = output_path

# Render the scene
bpy.ops.render.render(write_still=True)

