import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius to make it hollow)
inner_cone = trimesh.creation.cone(radius=18, height=35)

# Subtract inner cone from outer cone to create hollow cone
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and valid for 3D printing
hollow_cone.fill_holes()
hollow_cone.process()

# Export as STL using numpy-stl
vertices = hollow_cone.vertices
faces = hollow_cone.faces

# Create the mesh
stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        stl_mesh.vectors[i][j] = vertices[f[j], :]

# Write the mesh to file
stl_mesh.save('output.stl')