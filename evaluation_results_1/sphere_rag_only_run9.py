import trimesh
import numpy as np
from stl import mesh

# Create outer sphere (45mm radius)
outer_sphere = trimesh.creation.icosphere(radius=45)

# Create inner sphere (44mm radius to make 1mm wall thickness)
inner_sphere = trimesh.creation.icosphere(radius=44)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight (important for 3D printing)
hollow_sphere.fill_holes()
hollow_sphere.process()

# Convert to numpy-stl mesh
vertices = hollow_sphere.vertices
faces = hollow_sphere.faces
hollow_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        hollow_mesh.vectors[i][j] = vertices[f[j], :]

# Save as STL file
hollow_mesh.save('output.stl')