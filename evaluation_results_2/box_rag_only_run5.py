import trimesh
import numpy as np
from stl import mesh

# Create outer box dimensions (20x30x40mm)
outer_box = trimesh.creation.box(extents=[20, 30, 40])

# Create inner box dimensions (subtracting 2mm from each side for walls)
inner_box = trimesh.creation.box(extents=[20-4, 30-4, 40-2])

# Position the inner box centered within the outer box
inner_box.apply_translation([0, 0, 1])  # Raise by 1mm to leave bottom thickness

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight and valid for 3D printing
hollow_box.fill_holes()
hollow_box.fix_normals()

# Export as STL using numpy-stl
vertices = hollow_box.vertices
faces = hollow_box.faces

# Create the mesh
hollow_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        hollow_mesh.vectors[i][j] = vertices[f[j], :]

# Save to file
hollow_mesh.save('output.stl')