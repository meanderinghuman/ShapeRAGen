import numpy as np
import trimesh
from stl import mesh

# Create outer box dimensions (20x30x40mm)
outer_box = trimesh.primitives.Box(extents=[20, 30, 40])

# Create inner box dimensions (18x28x38mm for 1mm wall thickness)
inner_box = trimesh.primitives.Box(extents=[18, 28, 38])

# Position inner box at the center
inner_box.apply_translation([0, 0, 0])

# Create hollow box by subtracting inner from outer
hollow_mesh = outer_box.difference(inner_box)

# Ensure mesh is watertight and valid for 3D printing
hollow_mesh.process(validate=True)
hollow_mesh.fill_holes()

# Export as STL using numpy-stl
vertices = hollow_mesh.vertices
faces = hollow_mesh.faces

# Create the mesh
hollow_stl = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        hollow_stl.vectors[i][j] = vertices[f[j], :]

# Save the STL file
hollow_stl.save('output.stl')