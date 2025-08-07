import trimesh
import numpy as np
from stl import mesh

# Create outer sphere (radius 45mm)
outer_sphere = trimesh.creation.icosphere(radius=45)

# Create inner sphere (radius 44mm for 1mm wall thickness)
inner_sphere = trimesh.creation.icosphere(radius=44)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight (manifold) for printing
hollow_sphere.fill_holes()
hollow_sphere.fix_normals()

# Convert to numpy-stl mesh format
vertices = hollow_sphere.vertices
faces = hollow_sphere.faces

# Create the numpy-stl mesh object
numpy_stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        numpy_stl_mesh.vectors[i][j] = vertices[f[j], :]

# Save as STL file
numpy_stl_mesh.save('output.stl')