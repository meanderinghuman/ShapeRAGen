import trimesh
import numpy as np
from stl import mesh as stl_mesh

# Define outer dimensions
outer_length = 30.0  # x dimension
outer_width = 20.0   # y dimension
outer_height = 40.0  # z dimension
wall_thickness = 1.0  # 1mm wall thickness

# Create outer box
outer_box = trimesh.primitives.Box(extents=[outer_length, outer_width, outer_height])

# Calculate inner dimensions (subtracting wall thickness from both sides)
inner_length = outer_length - 2 * wall_thickness
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - wall_thickness  # only subtract from bottom for open-top box

# Create inner box (slightly smaller)
inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])

# Position inner box centered within outer box
inner_box.apply_translation([0, 0, wall_thickness/2])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure mesh is watertight (important for 3D printing)
hollow_box.fill_holes()
hollow_box.fix_normals()

# Convert trimesh to numpy-stl mesh
vertices = hollow_box.vertices
faces = hollow_box.faces
numpy_stl_mesh = stl_mesh.Mesh(np.zeros(faces.shape[0], dtype=stl_mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        numpy_stl_mesh.vectors[i][j] = vertices[f[j], :]

# Save as STL file
numpy_stl_mesh.save('output.stl')

# Optional: Show the mesh (requires pyglet)
# hollow_box.show()