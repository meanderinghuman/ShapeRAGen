import numpy as np
import trimesh
from stl import mesh

# Create outer box dimensions
outer_box = trimesh.creation.box(extents=[20, 30, 40])

# Create inner box dimensions (2mm wall thickness)
inner_box = trimesh.creation.box(extents=[16, 26, 38])

# Subtract inner box from outer box to create hollow box
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight and valid for 3D printing
hollow_box.fill_holes()
hollow_box.fix_normals()

# Export as STL using numpy-stl
vertices = hollow_box.vertices
faces = hollow_box.faces

# Create the mesh object
hollow_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        hollow_mesh.vectors[i][j] = vertices[f[j], :]

# Save the STL file
hollow_mesh.save('output.stl')