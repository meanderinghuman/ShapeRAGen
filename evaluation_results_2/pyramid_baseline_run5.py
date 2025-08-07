import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid
outer_vertices = np.array([
    [0, 0, 0],          # base vertex 1
    [25, 0, 0],         # base vertex 2
    [25, 25, 0],        # base vertex 3
    [0, 25, 0],         # base vertex 4
    [12.5, 12.5, 30]    # apex
])

outer_faces = np.array([
    [0, 1, 4],  # side 1
    [1, 2, 4],  # side 2
    [2, 3, 4],  # side 3
    [3, 0, 4],  # side 4
    [0, 3, 2],  # base triangle 1
    [0, 2, 1]   # base triangle 2
])

outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)

# Create inner pyramid (smaller version)
inner_scale = 0.8  # adjust this for wall thickness
inner_vertices = outer_vertices * inner_scale
inner_vertices[:, :2] += (1 - inner_scale) * 12.5  # center the inner pyramid
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=outer_faces)

# Ensure both meshes are watertight
outer_mesh.fix_normals()
outer_mesh.fill_holes()
inner_mesh.fix_normals()
inner_mesh.fill_holes()

# Create hollow pyramid using difference
hollow_pyramid = outer_mesh.difference(inner_mesh)

# Export as STL
hollow_pyramid.export('output.stl')