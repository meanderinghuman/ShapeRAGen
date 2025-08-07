import trimesh
import numpy as np
from stl import mesh

# Create outer box dimensions
outer_dimensions = [20, 30, 40]  # width, length, height in mm
wall_thickness = 2.0  # 2mm wall thickness for FDM printing

# Calculate inner box dimensions
inner_dimensions = [d - 2 * wall_thickness for d in outer_dimensions]

# Create outer and inner boxes
outer_box = trimesh.creation.box(outer_dimensions)
inner_box = trimesh.creation.box(inner_dimensions)

# Position the inner box centered within the outer box
inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight (important for 3D printing)
hollow_box.fill_holes()
hollow_box.process()

# Convert trimesh to numpy-stl mesh
vertices = hollow_box.vertices
faces = hollow_box.faces

# Create numpy-stl mesh object
data = np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype)
for i, f in enumerate(faces):
    for j in range(3):
        data['vectors'][i][j] = vertices[f[j], :]

numpy_mesh = mesh.Mesh(data)

# Save as STL file
numpy_mesh.save('output.stl')