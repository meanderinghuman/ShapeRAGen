import trimesh
import numpy as np
from stl import mesh as stl_mesh

# Create outer pyramid
outer_vertices = np.array([
    [0, 0, 0],        # base vertex 0
    [25, 0, 0],       # base vertex 1
    [25, 25, 0],      # base vertex 2
    [0, 25, 0],       # base vertex 3
    [12.5, 12.5, 30]  # apex
])

outer_faces = np.array([
    [0, 1, 4],  # side 1
    [1, 2, 4],  # side 2
    [2, 3, 4],  # side 3
    [3, 0, 4],  # side 4
    [0, 3, 2],  # base triangle 1
    [0, 2, 1]   # base triangle 2
])

outer_pyramid = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)

# Create inner pyramid (smaller by 2mm on each side)
inner_vertices = np.array([
    [2, 2, 0],        # base vertex 0
    [23, 2, 0],       # base vertex 1
    [23, 23, 0],      # base vertex 2
    [2, 23, 0],       # base vertex 3
    [12.5, 12.5, 28]  # apex (2mm below outer apex)
])

inner_faces = np.array([
    [0, 1, 4],  # side 1
    [1, 2, 4],  # side 2
    [2, 3, 4],  # side 3
    [3, 0, 4],  # side 4
    [0, 3, 2],  # base triangle 1
    [0, 2, 1]   # base triangle 2
])

inner_pyramid = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Combine meshes to create hollow pyramid
hollow_pyramid = outer_pyramid + inner_pyramid

# Export as STL
hollow_pyramid.export('output.stl')