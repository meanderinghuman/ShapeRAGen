import numpy as np
import trimesh
from stl import mesh as stl_mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius for hollow effect)
inner_cone = trimesh.creation.cone(radius=18, height=35)

# Subtract inner cone from outer cone to make it hollow
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight (important for 3D printing)
hollow_cone.fill_holes()
hollow_cone.process()

# Convert trimesh to numpy-stl mesh
vertices = hollow_cone.vertices
faces = hollow_cone.faces

# Create the STL mesh
stl_data = np.zeros(faces.shape[0], dtype=stl_mesh.Mesh.dtype)
for i, f in enumerate(faces):
    for j in range(3):
        stl_data['vectors'][i][j] = vertices[f[j], :]

# Create the mesh and save to file
cone_mesh = stl_mesh.Mesh(stl_data)
cone_mesh.save('output.stl')