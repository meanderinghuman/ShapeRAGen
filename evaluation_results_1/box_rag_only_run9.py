import trimesh
import numpy as np
from stl import mesh

# Create outer box dimensions
outer_box = trimesh.creation.box(extents=[20, 30, 40])

# Create inner box dimensions (2mm wall thickness)
inner_box = trimesh.creation.box(extents=[16, 26, 38])

# Hollow out the box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight and valid for 3D printing
hollow_box.fill_holes()
hollow_box.process()

# Convert trimesh object to numpy-stl mesh
vertices = hollow_box.vertices
faces = hollow_box.faces

# Create the mesh
stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        stl_mesh.vectors[i][j] = vertices[f[j], :]

# Write the mesh to file
stl_mesh.save('output.stl')