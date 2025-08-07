import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid
outer_vertices = np.array([
    [0, 0, 0],       # Base vertex 0
    [25, 0, 0],      # Base vertex 1
    [25, 25, 0],     # Base vertex 2
    [0, 25, 0],      # Base vertex 3
    [12.5, 12.5, 30] # Apex vertex 4
])

outer_faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [0, 3, 2],  # Base triangle 1
    [0, 2, 1]   # Base triangle 2
])

# Create inner pyramid (smaller by 2mm on each side)
inner_vertices = np.array([
    [2, 2, 0],       # Base vertex 0
    [23, 2, 0],      # Base vertex 1
    [23, 23, 0],     # Base vertex 2
    [2, 23, 0],      # Base vertex 3
    [12.5, 12.5, 28] # Apex vertex 4 (2mm below outer apex)
])

inner_faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [0, 3, 2],  # Base triangle 1
    [0, 2, 1]   # Base triangle 2
])

# Create mesh objects
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Create hollow pyramid by subtracting inner from outer
hollow_pyramid = outer_mesh.difference(inner_mesh)

# Ensure the mesh is watertight and valid for printing
hollow_pyramid.fill_holes()
hollow_pyramid.process()

# Export as STL
hollow_pyramid.export('output.stl')