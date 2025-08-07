import trimesh
import numpy as np
from stl import mesh

# Create outer sphere with radius 45mm
outer_sphere = trimesh.creation.icosphere(radius=45, subdivisions=3)

# Create inner sphere with slightly smaller radius (44mm for 1mm wall thickness)
inner_sphere = trimesh.creation.icosphere(radius=44, subdivisions=3)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight (manifold) for 3D printing
hollow_sphere.fill_holes()
hollow_sphere.process()

# Export as STL file
hollow_sphere.export('output.stl')

# Alternative method using numpy-stl to create the STL file
vertices = hollow_sphere.vertices
faces = hollow_sphere.faces

# Create the numpy-stl mesh object
numpy_stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        numpy_stl_mesh.vectors[i][j] = vertices[f[j], :]

# Save the STL file
numpy_stl_mesh.save('output.stl')