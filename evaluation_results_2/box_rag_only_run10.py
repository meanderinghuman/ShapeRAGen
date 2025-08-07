import trimesh
import numpy as np
from stl import mesh

# Dimensions (mm)
outer_length = 30
outer_width = 20
outer_height = 40
wall_thickness = 2  # Recommended for FDM printing

# Create outer box
outer_box = trimesh.creation.box((outer_length, outer_width, outer_height))

# Create inner box dimensions
inner_length = outer_length - 2 * wall_thickness
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - 2 * wall_thickness

# Create inner box (centered)
inner_box = trimesh.creation.box((inner_length, inner_width, inner_height))

# Position inner box at the same center as outer box
inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure mesh is watertight (important for 3D printing)
hollow_box.fill_holes()
hollow_box.process()

# Export as STL
hollow_box.export('output.stl')

# Convert to numpy-stl mesh for additional operations if needed
vertices = hollow_box.vertices
faces = hollow_box.faces
numpy_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        numpy_mesh.vectors[i][j] = vertices[f[j], :]

# Save using numpy-stl (alternative method)
numpy_mesh.save('output.stl')