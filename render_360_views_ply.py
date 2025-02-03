import sys, os
import json
import bpy
import mathutils
import numpy as np
import math
DEBUG = False

VIEWS = 500
RESOLUTION = 800
RESULTS_PATH = 'results'
DEPTH_SCALE = 1.4
COLOR_DEPTH = 8
FORMAT = 'PNG'
RANDOM_VIEWS = True
UPPER_VIEWS = True
CIRCLE_FIXED_START = (.3,0,0)

fp = bpy.path.abspath(f"//{RESULTS_PATH}")

# Path to the custom PLY file
ply_path = "./it3000-mc192.ply"

# Function to import PLY file and display vertex colors
def load_ply_with_colors(ply_path):
    # Import the PLY file using Blender's built-in operator
    bpy.ops.import_mesh.ply(filepath=ply_path)

    # Get the imported object
    imported_obj = bpy.context.selected_objects[0]  # Assume the first selected object is the one we just imported

    # Ensure that the object has vertex colors
    if imported_obj.type == 'MESH' and imported_obj.data.vertex_colors:
        color_layer = imported_obj.data.vertex_colors.active
    else:
        raise ValueError(f"The imported PLY file does not contain vertex colors.")

    return imported_obj, color_layer

# Load the PLY file and get the object and its vertex color layer
imported_obj, color_layer = load_ply_with_colors(ply_path)


#bpy.ops.wm.read_factory_settings(use_empty=True)

# If a default cube exists, delete it
if "Cube" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["Cube"], do_unlink=True)





# Create a material for the object and use vertex colors
material = bpy.data.materials.new(name="VertexColorMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes

# Clear existing nodes and add new nodes
nodes.clear()

# Add the "Attribute" node to pull the vertex color layer
attribute_node = nodes.new(type="ShaderNodeAttribute")
attribute_node.attribute_name = color_layer.name  # Use the active color layer name

# Add the "Principled BSDF" shader node
bsdf_node = nodes.new(type="ShaderNodeBsdfPrincipled")

# Connect the attribute node to the base color input of the BSDF shader
material.node_tree.links.new(attribute_node.outputs["Color"], bsdf_node.inputs["Base Color"])

# Add the "Material Output" node
output_node = nodes.new(type="ShaderNodeOutputMaterial")
material.node_tree.links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

# Assign the material to the imported object
imported_obj.data.materials.append(material)

# Apply camera, scene, and render settings
scene = bpy.context.scene
scene.render.resolution_x = RESOLUTION
scene.render.resolution_y = RESOLUTION
scene.render.resolution_percentage = 100

# Set up camera
cam = scene.objects.get('Camera')
if not cam:
    cam_data = bpy.data.cameras.new(name="Camera")
    cam = bpy.data.objects.new("Camera", cam_data)
    scene.collection.objects.link(cam)

cam.location = (0, 4.0, 0.5)
cam_constraint = cam.constraints.new(type='TRACK_TO')
cam_constraint.track_axis = 'TRACK_NEGATIVE_Z'
cam_constraint.up_axis = 'UP_Y'

# Render settings
scene.render.image_settings.file_format = FORMAT
scene.render.image_settings.color_depth = str(COLOR_DEPTH)

# Set up output folder
if not os.path.exists(fp):
    os.makedirs(fp)

# Rotate the object and render from different views
rotation_step = 360.0 / VIEWS
for i in range(VIEWS):
    angle = rotation_step * i
    imported_obj.rotation_euler[2] = math.radians(angle)
    
    # Set file path for rendering
    scene.render.filepath = os.path.join(fp, f"render_{i:03d}.png")
    
    # Render the scene
    bpy.ops.render.render(write_still=True)

    if DEBUG:
        break

# Optionally, save transforms as JSON
out_data = {'frames': []}
for i in range(VIEWS):
    frame_data = {
        'file_path': scene.render.filepath,
        'rotation': math.radians(rotation_step * i),
        'transform_matrix': list(imported_obj.matrix_world)
    }
    out_data['frames'].append(frame_data)

if not DEBUG:
    with open(os.path.join(fp, 'transforms.json'), 'w') as out_file:
        json.dump(out_data, out_file, indent=4)
