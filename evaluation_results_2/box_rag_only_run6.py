import numpy as np
import trimesh
from stl import mesh

# Outer dimensions
outer_length = 30.0  # mm
outer_width = 20.0   # mm
outer_height = 40.0  # mm
wall_thickness = 2.0  # mm (recommended minimum for FDM printing)

# Create outer box
outer_box = trimesh.primitives.Box(extents=[outer_length, outer_width, outer_height])

# Calculate inner dimensions
inner_length = outer_length - 2 * wall_thickness
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - 2 * wall_thickness

# Create inner box (hollow space)
inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])

# Subtract inner box from outer box to create hollow box
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight (manifold) for 3D printing
hollow_box = hollow_box.process(validate=True)

# Export using trimesh
hollow_box.export('output.stl')

# Alternative export using numpy-stl (for compatibility)
vertices = hollow_box.vertices
faces = hollow_box.faces

# Create the numpy-stl mesh object
stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        stl_mesh.vectors[i][j] = vertices[f[j], :]

# Write the mesh to file
stl_mesh.save('output.stl')