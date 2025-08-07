import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid
outer_vertices = np.array([
    [0, 0, 0],          # base vertex 0
    [25, 0, 0],         # base vertex 1
    [25, 25, 0],        # base vertex 2
    [0, 25, 0],         # base vertex 3
    [12.5, 12.5, 30]    # apex
])

outer_faces = np.array([
    [0, 1, 4],  # front face
    [1, 2, 4],  # right face
    [2, 3, 4],  # back face
    [3, 0, 4],  # left face
    [0, 3, 2],  # base triangle 1
    [0, 2, 1]   # base triangle 2
])

# Create inner pyramid (hollow space)
wall_thickness = 1.2
inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],
    [25 - wall_thickness, wall_thickness, 0],
    [25 - wall_thickness, 25 - wall_thickness, 0],
    [wall_thickness, 25 - wall_thickness, 0],
    [12.5, 12.5, 30 - wall_thickness]
])

inner_faces = np.array([
    [0, 1, 4],
    [1, 2, 4],
    [2, 3, 4],
    [3, 0, 4],
    [0, 3, 2],
    [0, 2, 1]
])

# Create mesh objects
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Subtract inner mesh from outer mesh to create hollow pyramid
hollow_pyramid = outer_mesh.difference(inner_mesh)

# Export as STL
hollow_pyramid.export('output.stl')