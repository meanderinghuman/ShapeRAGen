import numpy as np
import trimesh
from stl import mesh

# Create outer box dimensions
outer_dimensions = [30, 20, 40]  # x, y, z dimensions
wall_thickness = 2.0  # 2mm wall thickness

# Calculate inner box dimensions
inner_dimensions = [d - 2 * wall_thickness for d in outer_dimensions]

# Create outer and inner boxes
outer_box = trimesh.primitives.Box(extents=outer_dimensions)
inner_box = trimesh.primitives.Box(extents=inner_dimensions)

# Position inner box at the center
inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight and valid for 3D printing
hollow_box.process(validate=True)
hollow_box.fill_holes()

# Export as STL using numpy-stl
vertices = hollow_box.vertices
faces = hollow_box.faces

# Create the mesh
data = np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype)
for i, f in enumerate(faces):
    for j in range(3):
        data['vectors'][i][j] = vertices[f[j], :]

hollow_mesh = mesh.Mesh(data)
hollow_mesh.save('output.stl')