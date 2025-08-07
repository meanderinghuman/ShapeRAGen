import numpy as np
import trimesh
from stl import mesh

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],         # Base vertex 0
    [25, 0, 0],        # Base vertex 1
    [25, 25, 0],       # Base vertex 2
    [0, 25, 0],        # Base vertex 3
    [12.5, 12.5, 30]   # Apex vertex
])

# Create inner pyramid vertices (2mm offset from outer)
inner_vertices = np.array([
    [2, 2, 0],         # Base vertex 0
    [23, 2, 0],        # Base vertex 1
    [23, 23, 0],       # Base vertex 2
    [2, 23, 0],        # Base vertex 3
    [12.5, 12.5, 28]   # Apex vertex (2mm shorter)
])

# Define faces for outer pyramid (4 triangular sides + square base)
outer_faces = np.array([
    [0, 1, 4],    # Front face
    [1, 2, 4],    # Right face
    [2, 3, 4],    # Back face
    [3, 0, 4],    # Left face
    [0, 3, 2],    # Base triangle 1
    [0, 2, 1]     # Base triangle 2
])

# Define faces for inner pyramid (same structure as outer)
inner_faces = np.array([
    [0, 1, 4],    # Front face
    [1, 2, 4],    # Right face
    [2, 3, 4],    # Back face
    [3, 0, 4],    # Left face
    [0, 3, 2],    # Base triangle 1
    [0, 2, 1]     # Base triangle 2
])

# Create outer and inner meshes
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Create the hollow pyramid by subtracting inner from outer
hollow_pyramid = outer_mesh.difference(inner_mesh)

# Ensure the mesh is watertight and suitable for printing
hollow_pyramid.fill_holes()
hollow_pyramid.update_faces(hollow_pyramid.nondegenerate_faces())
hollow_pyramid.update_faces(hollow_pyramid.unique_faces())
hollow_pyramid.remove_unreferenced_vertices()

# Export as STL
hollow_pyramid.export('output.stl')