import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius for hollow effect)
inner_cone = trimesh.creation.cone(radius=18, height=35)

# Subtract inner cone from outer cone to create hollow cone
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and manifold for printing
hollow_cone.fill_holes()
hollow_cone.update_faces(hollow_cone.nondegenerate_faces())
hollow_cone.update_faces(hollow_cone.unique_faces())
hollow_cone.remove_unreferenced_vertices()

# Convert to numpy-stl mesh and save
vertices = hollow_cone.vertices
faces = hollow_cone.faces
numpy_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        numpy_mesh.vectors[i][j] = vertices[f[j], :]

numpy_mesh.save('output.stl')