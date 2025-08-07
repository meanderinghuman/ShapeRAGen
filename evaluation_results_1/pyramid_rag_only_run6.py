import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid vertices
outer_vertices = np.array([
    [0, 0, 0],       # Base vertex 0
    [25, 0, 0],      # Base vertex 1
    [25, 25, 0],     # Base vertex 2
    [0, 25, 0],      # Base vertex 3
    [12.5, 12.5, 30] # Apex vertex
])

# Create inner pyramid vertices (offset by 2mm for wall thickness)
inner_vertices = np.array([
    [2, 2, 0],       # Base vertex 0
    [23, 2, 0],      # Base vertex 1
    [23, 23, 0],     # Base vertex 2
    [2, 23, 0],      # Base vertex 3
    [12.5, 12.5, 28] # Apex vertex (2mm lower than outer)
])

# Define faces for outer pyramid
outer_faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [0, 3, 2],  # Base face 1
    [0, 2, 1]   # Base face 2
])

# Define faces for inner pyramid (inverted normals)
inner_faces = np.array([
    [4, 1, 0],  # Front face
    [4, 2, 1],  # Right face
    [4, 3, 2],  # Back face
    [4, 0, 3],  # Left face
    [2, 3, 0],  # Base face 1
    [1, 2, 0]   # Base face 2
])

# Create outer and inner meshes
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Combine meshes to create hollow pyramid
hollow_pyramid = trimesh.util.concatenate([outer_mesh, inner_mesh])

# Ensure mesh is watertight and valid for 3D printing
hollow_pyramid = hollow_pyramid.process(validate=True)

# Export as STL file
hollow_pyramid.export('output.stl')