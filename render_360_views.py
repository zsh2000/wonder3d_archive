import sys, os
import json
import bpy
import mathutils
import numpy as np
import bmesh

DEBUG = False

VIEWS = 10
RESOLUTION = 256
RESULTS_PATH = 'results_0'
DEPTH_SCALE = 1.4
COLOR_DEPTH = 8
FORMAT = 'PNG'
RANDOM_VIEWS = False
UPPER_VIEWS = False
CIRCLE_FIXED_START = (.3,0,0)

fp = bpy.path.abspath(f"//{RESULTS_PATH}")

# Path to the custom OBJ file
obj_path = "/home/zheng720/wonder3d/Wonder3D/instant-nsr-pl/exp/0_alpha/@20241108-125452/save/it3000-mc192.obj"
#obj_path = "./it3000-mc192.ply"

# Function to parse custom OBJ with vertex colors
def load_custom_obj_with_colors(obj_path):
    verts = []
    faces = []
    colors = []
    
    with open(obj_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()
                x, y, z = map(float, parts[1:4])
                r, g, b = map(float, parts[4:7])
                verts.append((x, y, z))
                colors.append((r, g, b, 1.0))  # Add alpha = 1.0
            elif line.startswith('f '):
                face = [int(p.split('/')[0]) - 1 for p in line.strip().split()[1:]]
                faces.append(face)

    # Create a new mesh and object in Blender
    mesh = bpy.data.meshes.new(name="ColoredMesh")
    obj = bpy.data.objects.new(name="ColoredObject", object_data=mesh)
    bpy.context.collection.objects.link(obj)
    
    # Set the mesh vertices and faces
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    # Assign vertex colors
    if mesh.vertex_colors:
        color_layer = mesh.vertex_colors["Col"]
    else:
        color_layer = mesh.vertex_colors.new(name="Col")

    # Populate vertex colors
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.faces.ensure_lookup_table()
    for face in bm.faces:
        for loop, vert_idx in zip(face.loops, face.verts):
            loop_idx = loop.index
            color_layer.data[loop_idx].color = colors[vert_idx.index]
    
    bm.to_mesh(mesh)
    bm.free()
    
    return obj

# Load the OBJ file and apply vertex colors
loaded_obj = load_custom_obj_with_colors(obj_path)

# # If a default cube exists, delete it
# if "Cube" in bpy.data.objects:
#     bpy.data.objects.remove(bpy.data.objects["Cube"], do_unlink=True)

bpy.ops.wm.read_factory_settings(use_empty=True)


# Apply a material to display vertex colors
material = bpy.data.materials.new(name="VertexColorMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes

# Clear existing nodes and add new nodes
nodes.clear()

# Add the "Attribute" node to pull the vertex color layer
attribute_node = nodes.new(type="ShaderNodeAttribute")
attribute_node.attribute_name = "Col"  # Match the color layer name

# Add the "Principled BSDF" shader node
bsdf_node = nodes.new(type="ShaderNodeBsdfPrincipled")

# Connect the attribute node to the base color input of the BSDF shader
material.node_tree.links.new(attribute_node.outputs["Color"], bsdf_node.inputs["Base Color"])

# Add the "Material Output" node
output_node = nodes.new(type="ShaderNodeOutputMaterial")
material.node_tree.links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

# Assign the material to the object
loaded_obj.data.materials.append(material)

# Add Camera, Scene, and Render settings

def listify_matrix(matrix):
    matrix_list = []
    for row in matrix:
        matrix_list.append(list(row))
    return matrix_list

if not os.path.exists(fp):
    os.makedirs(fp)

out_data = {
    'camera_angle_x': bpy.data.objects['Camera'].data.angle_x,
}

bpy.context.scene.render.use_persistent_data = True

bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links

render_layers = tree.nodes.new('CompositorNodeRLayers')

depth_file_output = tree.nodes.new(type="CompositorNodeOutputFile")
depth_file_output.label = 'Depth Output'
if FORMAT == 'OPEN_EXR':
    links.new(render_layers.outputs['Depth'], depth_file_output.inputs[0])
else:
    map_node = tree.nodes.new(type="CompositorNodeMapValue")
    map_node.offset = [-0.7]
    map_node.size = [DEPTH_SCALE]
    map_node.use_min = True
    map_node.min = [0]
    links.new(render_layers.outputs['Depth'], map_node.inputs[0])
    links.new(map_node.outputs[0], depth_file_output.inputs[0])

normal_file_output = tree.nodes.new(type="CompositorNodeOutputFile")
normal_file_output.label = 'Normal Output'
links.new(render_layers.outputs['Normal'], normal_file_output.inputs[0])

bpy.context.scene.render.dither_intensity = 0.0
bpy.context.scene.render.film_transparent = True

objs = [ob for ob in bpy.context.scene.objects if ob.type in ('EMPTY') and 'Empty' in ob.name]
bpy.ops.object.delete({"selected_objects": objs})

def parent_obj_to_camera(b_camera):
    origin = (0, 0, 0)
    b_empty = bpy.data.objects.new("Empty", None)
    b_empty.location = origin
    b_camera.parent = b_empty
    scn = bpy.context.scene
    scn.collection.objects.link(b_empty)
    bpy.context.view_layer.objects.active = b_empty
    return b_empty

scene = bpy.context.scene
scene.render.resolution_x = RESOLUTION
scene.render.resolution_y = RESOLUTION
scene.render.resolution_percentage = 100

cam = scene.objects['Camera']
cam.location = (0, 4.0, 0.5)
cam_constraint = cam.constraints.new(type='TRACK_TO')
cam_constraint.track_axis = 'TRACK_NEGATIVE_Z'
cam_constraint.up_axis = 'UP_Y'
b_empty = parent_obj_to_camera(cam)
cam_constraint.target = b_empty

scene.render.image_settings.file_format = 'PNG'

stepsize = 360.0 / VIEWS
rotation_mode = 'XYZ'

if not DEBUG:
    for output_node in [depth_file_output, normal_file_output]:
        output_node.base_path = ''

out_data['frames'] = []

if not RANDOM_VIEWS:
    b_empty.rotation_euler = CIRCLE_FIXED_START

for i in range(0, VIEWS):
    if DEBUG:
        i = np.random.randint(0,VIEWS)
        b_empty.rotation_euler[2] += radians(stepsize*i)
    if RANDOM_VIEWS:
        scene.render.filepath = fp + '/r_' + str(i)
        if UPPER_VIEWS:
            rot = np.random.uniform(0, 1, size=3) * (1,0,2*np.pi)
            rot[0] = np.abs(np.arccos(1 - 2 * rot[0]) - np.pi/2)
            b_empty.rotation_euler = rot
        else:
            b_empty.rotation_euler = np.random.uniform(0, 2*np.pi, size=3)
    else:
        scene.render.filepath = fp + '/r_' + str(i)

    bpy.ops.render.render(write_still=True)

    frame_data = {
        'file_path': scene.render.filepath,
        'rotation': radians(stepsize),
        'transform_matrix': listify_matrix(cam.matrix_world)
    }
    out_data['frames'].append(frame_data)

    if RANDOM_VIEWS:
        if UPPER_VIEWS:
            rot = np.random.uniform(0, 1, size=3) * (1,0,2*np.pi)
            rot[0] = np.abs(np.arccos(1 - 2 * rot[0]) - np.pi/2)
            b_empty.rotation_euler = rot
        else:
            b_empty.rotation_euler = np.random.uniform(0, 2*np.pi, size=3)
    else:
        b_empty.rotation_euler[2] += radians(stepsize)

if not DEBUG:
    with open(fp + '/' + 'transforms.json', 'w') as out_file:
        json.dump(out_data, out_file, indent=4)
