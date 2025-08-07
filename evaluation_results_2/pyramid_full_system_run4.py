import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid
outer_vertices = np.array([
    [0, 0, 0],         # base vertex 0
    [25, 0, 0],        # base vertex 1
    [25, 25, 0],       # base vertex 2
    [0, 25, 0],        # base vertex 3
    [12.5, 12.5, 30]   # apex
])

outer_faces = np.array([
    [0, 1, 4],  # front face
    [1, 2, 4],  # right face
    [2, 3, 4],  # back face
    [3, 0, 4],  # left face
    [0, 3, 2],  # base triangle 1
    [0, 2, 1]   # base triangle 2
])

# Create inner pyramid (offset by 2mm for wall thickness)
inner_vertices = np.array([
    [2, 2, 0],         # base vertex 0
    [23, 2, 0],        # base vertex 1
    [23, 23, 0],       # base vertex 2
    [2, 23, 0],        # base vertex 3
    [12.5, 12.5, 28]   # apex (2mm below outer apex)
])

inner_faces = np.array([
    [0, 4, 1],  # front face (note reversed normal)
    [1, 4, 2],  # right face
    [2, 4, 3],  # back face
    [3, 4, 0],  # left face
    [0, 2, 3],  # base triangle 1
    [0, 1, 2]   # base triangle 2
])

# Create mesh objects
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Combine meshes to create hollow pyramid
hollow_pyramid = trimesh.util.concatenate([outer_mesh, inner_mesh])

# Ensure mesh is watertight and valid for printing
hollow_pyramid = hollow_pyramid.process(validate=True)

# Export as STL
hollow_pyramid.export('output.stl')