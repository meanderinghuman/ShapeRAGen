import trimesh
import numpy as np
from stl import mesh as stl_mesh

# Create outer pyramid
outer_vertices = np.array([
    [0, 0, 0],         # base vertex 0
    [25, 0, 0],        # base vertex 1
    [25, 25, 0],       # base vertex 2
    [0, 25, 0],        # base vertex 3
    [12.5, 12.5, 30]   # apex
])

outer_faces = np.array([
    [0, 1, 4],  # side face 1
    [1, 2, 4],   # side face 2
    [2, 3, 4],   # side face 3
    [3, 0, 4],   # side face 4
    [0, 3, 2],   # base face 1
    [0, 2, 1]    # base face 2
])

outer_pyramid = trimesh.Trimesh(vertices=outer_vertices, faces=outer_faces)

# Create inner pyramid by scaling down the outer pyramid
inner_pyramid = outer_pyramid.copy()
inner_pyramid.vertices *= 0.8  # scale down to 80% size
inner_pyramid.vertices[:, 2] = outer_pyramid.vertices[:, 2]  # keep original height

# Create hollow pyramid by combining outer and inner meshes
hollow_pyramid = trimesh.util.concatenate([
    outer_pyramid,
    inner_pyramid
])

# Ensure the mesh is watertight and valid for 3D printing
hollow_pyramid = hollow_pyramid.process()

# Export as STL
hollow_pyramid.export('output.stl')