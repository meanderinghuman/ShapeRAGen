import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid vertices
base_size = 25
height = 30
outer_vertices = np.array([
    [0, 0, 0],                     # Base vertex 0
    [base_size, 0, 0],             # Base vertex 1
    [base_size, base_size, 0],     # Base vertex 2
    [0, base_size, 0],             # Base vertex 3
    [base_size/2, base_size/2, height]  # Apex vertex
])

# Create inner pyramid vertices (smaller by 2mm wall thickness)
wall_thickness = 2
inner_size = base_size - 2 * wall_thickness
inner_height = height - wall_thickness
inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],
    [base_size - wall_thickness, wall_thickness, 0],
    [base_size - wall_thickness, base_size - wall_thickness, 0],
    [wall_thickness, base_size - wall_thickness, 0],
    [base_size/2, base_size/2, inner_height]
])

# Define faces for the pyramids (same for both)
faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [0, 3, 1],  # Base triangle 1
    [1, 3, 2]   # Base triangle 2
])

# Create outer and inner meshes
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=faces)

# Create hollow pyramid by subtracting inner from outer
hollow_pyramid = outer_mesh.difference(inner_mesh)

# Ensure the mesh is watertight and valid for printing
hollow_pyramid.fill_holes()
hollow_pyramid.process()

# Export as STL
hollow_pyramid.export('output.stl')