import trimesh
import numpy as np
from stl import mesh

# Create outer sphere with radius 45mm
outer_sphere = trimesh.creation.icosphere(radius=45, subdivisions=3)

# Create inner sphere with slightly smaller radius (40mm) to make it hollow with 5mm wall thickness
inner_sphere = trimesh.creation.icosphere(radius=40, subdivisions=3)

# Create the hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight (important for 3D printing)
hollow_sphere.fill_holes()
hollow_sphere.process()

# Export as STL file
hollow_sphere.export('output.stl')

# Alternatively, using numpy-stl to save the file
vectors = hollow_sphere.triangles
stl_mesh = mesh.Mesh(np.zeros(vectors.shape[0], dtype=mesh.Mesh.dtype))
stl_mesh.vectors = vectors
stl_mesh.save('output.stl')