import trimesh
import numpy as np
from stl import mesh

# Create outer box
outer_box = trimesh.primitives.Box(extents=[20, 30, 40])

# Create inner box (hollow space) with 2mm wall thickness
inner_box = trimesh.primitives.Box(extents=[16, 26, 38])

# Position inner box centered within outer box
inner_box.apply_translation([0, 0, 0])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure mesh is watertight and manifold for printing
hollow_box.fill_holes()
hollow_box.fix_normals()

# Export as STL using numpy-stl
vertices = hollow_box.vertices
faces = hollow_box.faces

# Create the mesh
stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        stl_mesh.vectors[i][j] = vertices[f[j], :]

# Write the mesh to file
stl_mesh.save('output.stl')