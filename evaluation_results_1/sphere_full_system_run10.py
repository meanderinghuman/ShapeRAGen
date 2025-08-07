import trimesh
import numpy as np
from stl import mesh

# Create outer sphere with radius 45mm
outer_sphere = trimesh.primitives.Sphere(radius=45)

# Create inner sphere with slightly smaller radius (44mm wall thickness)
inner_sphere = trimesh.primitives.Sphere(radius=44)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight (important for 3D printing)
hollow_sphere.fill_holes()
hollow_sphere.process()

# Convert to numpy-stl mesh format
stl_mesh = mesh.Mesh(np.zeros(hollow_sphere.faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(hollow_sphere.faces):
    for j in range(3):
        stl_mesh.vectors[i][j] = hollow_sphere.vertices[f[j]]

# Save the STL file
stl_mesh.save('output.stl')