import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (for hollow space) with slightly smaller radius
inner_cone = trimesh.creation.cone(radius=18, height=34.9)  # Slightly shorter to ensure manifold mesh

# Position inner cone slightly above base to ensure proper wall thickness
inner_cone.apply_translation([0, 0, 0.1])

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and suitable for printing
hollow_cone.fill_holes()
hollow_cone.process()

# Export as STL using numpy-stl
vertices = hollow_cone.vertices
faces = hollow_cone.faces

# Create the mesh object
stl_mesh_obj = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

# Fill the mesh object with vertex and face data
for i, f in enumerate(faces):
    for j in range(3):
        stl_mesh_obj.vectors[i][j] = vertices[f[j], :]

# Write the mesh to file
stl_mesh_obj.save('output.stl')