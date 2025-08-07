import trimesh
import numpy as np
from stl import mesh as stl_mesh

# Parameters
base_size = 25.0
height = 30.0
wall_thickness = 2.0

# Create outer pyramid
outer_vertices = np.array([
    [0, 0, 0],
    [base_size, 0, 0],
    [base_size, base_size, 0],
    [0, base_size, 0],
    [base_size/2, base_size/2, height]
])

outer_faces = np.array([
    [0, 1, 4],
    [1, 2, 4],
    [2, 3, 4],
    [3, 0, 4],
    [0, 3, 2],
    [0, 2, 1]
])

outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)

# Create inner pyramid (smaller by wall thickness)
inner_size = base_size - 2 * wall_thickness
inner_height = height - wall_thickness

inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],
    [wall_thickness + inner_size, wall_thickness, 0],
    [wall_thickness + inner_size, wall_thickness + inner_size, 0],
    [wall_thickness, wall_thickness + inner_size, 0],
    [base_size/2, base_size/2, inner_height]
])

inner_faces = np.array([
    [0, 1, 4],
    [1, 2, 4],
    [2, 3, 4],
    [3, 0, 4],
    [0, 3, 2],
    [0, 2, 1]
])

inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Combine meshes to create hollow pyramid
hollow_pyramid = trimesh.util.concatenate([outer_mesh, inner_mesh])

# Ensure mesh is watertight and export
hollow_pyramid.fill_holes()
hollow_pyramid.export('output.stl')