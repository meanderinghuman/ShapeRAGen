import trimesh
import numpy as np
from stl import mesh

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

# Create inner pyramid (smaller by 2mm for wall thickness)
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

# Create mesh objects
outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Create hollow pyramid by subtracting inner from outer
hollow_pyramid = outer_mesh.difference(inner_mesh)

# Repair mesh to ensure it's manifold and watertight
hollow_pyramid.process()

# Export as STL
hollow_pyramid.export('output.stl')