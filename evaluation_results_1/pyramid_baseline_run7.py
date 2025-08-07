import trimesh
import numpy as np
from stl import mesh

# Parameters
base_size = 25.0  # mm
height = 30.0     # mm
wall_thickness = 2.0  # mm

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],  # base vertex 0
    [base_size, 0, 0],  # base vertex 1
    [base_size, base_size, 0],  # base vertex 2
    [0, base_size, 0],  # base vertex 3
    [base_size/2, base_size/2, height]  # apex
])

# Create inner pyramid vertices (offset by wall thickness)
inner_size = base_size - 2 * wall_thickness
inner_height = height - wall_thickness
inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],
    [base_size - wall_thickness, wall_thickness, 0],
    [base_size - wall_thickness, base_size - wall_thickness, 0],
    [wall_thickness, base_size - wall_thickness, 0],
    [base_size/2, base_size/2, inner_height]
])

# Faces for a pyramid (4 triangular sides + 1 square base)
faces = [
    [0, 1, 4],  # front face
    [1, 2, 4],  # right face
    [2, 3, 4],  # back face
    [3, 0, 4],  # left face
    [0, 3, 2], [0, 2, 1]  # base (two triangles)
]

# Create outer and inner meshes
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=faces)

# Combine meshes to create hollow pyramid
hollow_pyramid = outer_mesh + inner_mesh

# Ensure the mesh is watertight and valid for printing
hollow_pyramid.fill_holes()
hollow_pyramid.process()

# Export as STL
hollow_pyramid.export('output.stl')