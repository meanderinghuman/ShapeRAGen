import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid
outer_vertices = np.array([
    [0, 0, 0], [25, 0, 0], [25, 25, 0], [0, 25, 0],  # base vertices
    [12.5, 12.5, 30]  # apex
])
outer_faces = np.array([
    [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],  # sides
    [0, 3, 2], [0, 2, 1]  # base
])
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)

# Create smaller inner pyramid (hollow space)
inner_vertices = np.array([
    [2, 2, 0], [23, 2, 0], [23, 23, 0], [2, 23, 0],  # base vertices
    [12.5, 12.5, 28]  # apex (slightly lower than outer)
])
inner_faces = np.array([
    [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],  # sides
    [0, 3, 2], [0, 2, 1]  # base
])
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Combine meshes to create hollow pyramid
hollow_pyramid = outer_mesh + inner_mesh

# Ensure the mesh is watertight and export
hollow_pyramid.fill_holes()
hollow_pyramid.export('output.stl')