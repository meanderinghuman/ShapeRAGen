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

# Create inner pyramid (smaller by wall thickness)
wall_thickness = 2.0
inner_vertices = np.array([
    [wall_thickness, wall_thickness, 0],
    [25-wall_thickness, wall_thickness, 0],
    [25-wall_thickness, 25-wall_thickness, 0],
    [wall_thickness, 25-wall_thickness, 0],
    [12.5, 12.5, 30-wall_thickness]
])
inner_faces = np.array([
    [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],  # sides
    [0, 3, 2], [0, 2, 1]  # base
])
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Combine meshes to create hollow pyramid
hollow_pyramid = trimesh.util.concatenate([outer_mesh, inner_mesh])

# Export as STL
hollow_pyramid.export('output.stl')