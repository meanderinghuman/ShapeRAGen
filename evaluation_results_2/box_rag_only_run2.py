import trimesh
import numpy as np
from stl import mesh

# Create outer box dimensions (20x30x40mm)
outer_box = trimesh.creation.box(extents=[20, 30, 40])

# Create inner box dimensions (18x28x39mm to maintain 1mm wall thickness)
# Slightly shorter in Z to ensure printable bottom layer
inner_box = trimesh.creation.box(extents=[18, 28, 39])

# Center both boxes
outer_box.apply_translation([-10, -15, -20])
inner_box.apply_translation([-9, -14, -19.5])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure mesh is watertight and valid for printing
hollow_box.fill_holes()
hollow_box.process()

# Export as STL using numpy-stl
vertices = hollow_box.vertices
faces = hollow_box.faces

# Create the mesh
hollow_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        hollow_mesh.vectors[i][j] = vertices[f[j], :]

# Write the mesh to file "output.stl"
hollow_mesh.save('output.stl')