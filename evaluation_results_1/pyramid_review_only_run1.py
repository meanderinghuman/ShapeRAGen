import trimesh
import numpy as np

base_size = 25.0
height = 30.0
wall_thickness = 1.0

outer_vertices = np.array([
    [0, 0, 0],
    [base_size, 0, 0],
    [base_size, base_size, 0],
    [0, base_size, 0],
    [base_size/2, base_size/2, height]
])

inner_size = base_size - 2 * wall_thickness
inner_height = height - wall_thickness
inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],
    [base_size - wall_thickness, wall_thickness, 0],
    [base_size - wall_thickness, base_size - wall_thickness, 0],
    [wall_thickness, base_size - wall_thickness, 0],
    [base_size/2, base_size/2, inner_height]
])

faces = [
    [0, 1, 4],
    [1, 2, 4],
    [2, 3, 4],
    [3, 0, 4],
    [0, 3, 2], [0, 2, 1]
]

outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=faces)

hollow_pyramid = trimesh.boolean.difference([outer_mesh, inner_mesh])

if not hollow_pyramid.is_watertight:
    hollow_pyramid.fill_holes()
    hollow_pyramid.fix_normals()

hollow_pyramid.export('output.stl')