import trimesh
import numpy as np
from stl import mesh as stl_mesh

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40)

# Create inner cylinder (hollow part) with slightly smaller radius
inner_cylinder = trimesh.creation.cylinder(radius=14, height=40.1)  # Slightly taller to ensure clean boolean

# Subtract inner cylinder from outer cylinder to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure the mesh is watertight (important for 3D printing)
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Export as STL using numpy-stl
vertices = hollow_cylinder.vertices
faces = hollow_cylinder.faces

# Create the mesh object for numpy-stl
stl_mesh_obj = stl_mesh.Mesh(np.zeros(faces.shape[0], dtype=stl_mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        stl_mesh_obj.vectors[i][j] = vertices[f[j], :]

# Save the STL file
stl_mesh_obj.save('output.stl')