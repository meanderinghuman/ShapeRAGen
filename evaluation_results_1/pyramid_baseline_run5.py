import trimesh
import numpy as np

# Create outer pyramid
outer_vertices = np.array([
    [0, 0, 0],       # base vertex 0
    [25, 0, 0],      # base vertex 1
    [25, 25, 0],     # base vertex 2
    [0, 25, 0],      # base vertex 3
    [12.5, 12.5, 30] # apex
])

outer_faces = np.array([
    [0, 1, 4],  # side face 1
    [1, 2, 4],  # side face 2
    [2, 3, 4],  # side face 3
    [3, 0, 4],  # side face 4
    [0, 3, 2],  # base face 1
    [0, 2, 1]   # base face 2
])

outer_mesh = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)

# Create inner pyramid (smaller version)
inner_scale = 0.8  # scale factor for inner pyramid
inner_vertices = outer_vertices * inner_scale
# Center the inner pyramid
inner_vertices[:, :2] += (1 - inner_scale) * 12.5

inner_faces = outer_faces.copy()  # same face structure
inner_mesh = trimesh.Trimesh(vertices=inner_vertices, faces=inner_faces)

# Ensure both meshes are watertight
outer_mesh.fix_normals()
outer_mesh.fill_holes()
inner_mesh.fix_normals()
inner_mesh.fill_holes()

# Create hollow pyramid by difference
hollow_pyramid = outer_mesh.difference(inner_mesh)

# Export as STL
hollow_pyramid.export('output.stl')