import trimesh
import numpy as np
from stl import mesh

# Create outer cone (larger radius)
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius, making the wall thickness 2mm)
inner_cone = trimesh.creation.cone(radius=18, height=35)

# Move inner cone up slightly to ensure proper boolean operation
inner_cone.apply_translation([0, 0, 0.1])

# Subtract inner cone from outer cone to create hollow cone
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight and valid for 3D printing
hollow_cone.fill_holes()
hollow_cone.process()

# Convert trimesh object to numpy-stl mesh
vertices = hollow_cone.vertices
faces = hollow_cone.faces

# Create the numpy-stl mesh object
data = np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype)
for i, f in enumerate(faces):
    for j in range(3):
        data['vectors'][i][j] = vertices[f[j], :]

numpy_mesh = mesh.Mesh(data)

# Save the STL file
numpy_mesh.save('output.stl')