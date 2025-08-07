import trimesh
import numpy as np
from stl import mesh

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40)

# Create inner cylinder (for hollow space) with slightly smaller radius
inner_cylinder = trimesh.creation.cylinder(radius=14, height=40.1)  # Slightly taller to ensure clean boolean operation

# Subtract inner cylinder from outer cylinder to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure the mesh is watertight (important for 3D printing)
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Convert to numpy-stl mesh format
vertices = hollow_cylinder.vertices
faces = hollow_cylinder.faces
numpy_stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        numpy_stl_mesh.vectors[i][j] = vertices[f[j], :]

# Save as STL file
numpy_stl_mesh.save('output.stl')