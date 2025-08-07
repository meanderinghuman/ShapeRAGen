import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid
outer_vertices = np.array([
    [0, 0, 0],       # Base vertex 1
    [25, 0, 0],      # Base vertex 2
    [25, 25, 0],     # Base vertex 3
    [0, 25, 0],      # Base vertex 4
    [12.5, 12.5, 30] # Apex
])

outer_faces = np.array([
    [0, 1, 4],  # Front face
    [1, 2, 4],  # Right face
    [2, 3, 4],  # Back face
    [3, 0, 4],  # Left face
    [0, 3, 2],  # Base triangle 1
    [0, 2, 1]   # Base triangle 2
])

# Create inner pyramid (smaller by 2mm for wall thickness)
inner_vertices = np.array([
    [2, 2, 0],       # Base vertex 1
    [23, 2, 0],      # Base vertex 2
    [23, 23, 0],     # Base vertex 3
    [2, 23, 0],      # Base vertex 4
    [12.5, 12.5, 28] # Apex (2mm below outer apex)
])

inner_faces = np.array([
    [0, 4, 1],  # Front face (inverted normal)
    [1, 4, 2],  # Right face (inverted normal)
    [2, 4, 3],  # Back face (inverted normal)
    [3, 4, 0],  # Left face (inverted normal)
    [0, 2, 3],  # Base triangle 1 (inverted normal)
    [0, 1, 2]   # Base triangle 2 (inverted normal)
])

# Create mesh objects
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Combine meshes to create hollow pyramid
hollow_pyramid = trimesh.util.concatenate([outer_mesh, inner_mesh])

# Ensure the mesh is watertight and valid for 3D printing
hollow_pyramid.fill_holes()
hollow_pyramid.process()

# Export as STL
hollow_pyramid.export('output.stl')