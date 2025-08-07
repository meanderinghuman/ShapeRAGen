import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid (solid)
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

# Create inner pyramid (scaled down version)
scale_factor = 0.8  # adjust this to control wall thickness
inner_vertices = outer_vertices.copy()
inner_vertices[:-1] = inner_vertices[:-1] * scale_factor  # scale base vertices
inner_vertices[-1][2] = inner_vertices[-1][2] * 0.9       # slightly lower apex

inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=outer_faces)

# Ensure both meshes are watertight
outer_mesh.fill_holes()
outer_mesh.fix_normals()
inner_mesh.fill_holes()
inner_mesh.fix_normals()

# Create hollow pyramid by difference
hollow_pyramid = outer_mesh.difference(inner_mesh)

# Export as STL
hollow_pyramid.export('output.stl')