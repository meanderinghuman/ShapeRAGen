import trimesh
import numpy as np
from stl import mesh

# Create outer sphere (45mm radius)
outer_sphere = trimesh.creation.icosphere(radius=45)

# Create inner sphere (43mm radius for 2mm wall thickness)
inner_sphere = trimesh.creation.icosphere(radius=43)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight (manifold) for printing
hollow_sphere.fill_holes()
hollow_sphere.process()

# Convert to numpy-stl mesh
vertices = hollow_sphere.vertices
faces = hollow_sphere.faces
numpy_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        numpy_mesh.vectors[i][j] = vertices[f[j], :]

# Save as STL file
numpy_mesh.save('output.stl')