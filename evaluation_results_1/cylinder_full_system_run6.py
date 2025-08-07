import trimesh
import numpy as np
from stl import mesh

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40)

# Create inner cylinder (with slightly smaller radius to make it hollow)
inner_cylinder = trimesh.creation.cylinder(radius=14, height=40)  # 1mm wall thickness

# Subtract inner cylinder from outer cylinder to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure the mesh is watertight (important for 3D printing)
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Export as STL file using numpy-stl
vertices = hollow_cylinder.vertices
faces = hollow_cylinder.faces

# Create the mesh
hollow_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        hollow_mesh.vectors[i][j] = vertices[f[j], :]

# Write the mesh to file "output.stl"
hollow_mesh.save('output.stl')