import trimesh
import numpy as np
from stl import mesh

# Create a solid sphere with radius 45mm
solid_sphere = trimesh.primitives.Sphere(radius=45)

# Create a hollow sphere by subtracting a slightly smaller sphere
hollow_sphere = solid_sphere.difference(trimesh.primitives.Sphere(radius=44))

# Ensure the mesh is watertight (important for 3D printing)
hollow_sphere.process()

# Convert trimesh object to numpy-stl mesh
faces = hollow_sphere.faces
vertices = hollow_sphere.vertices

# Create the numpy-stl mesh object
numpy_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        numpy_mesh.vectors[i][j] = vertices[f[j], :]

# Save the STL file
numpy_mesh.save('output.stl')