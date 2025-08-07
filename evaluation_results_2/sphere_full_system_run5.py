import trimesh
import numpy as np
from stl import mesh

# Create hollow sphere with 1mm wall thickness (printable)
outer_sphere = trimesh.creation.icosphere(radius=45, subdivisions=3)
inner_sphere = trimesh.creation.icosphere(radius=44, subdivisions=3)

# Create hollow sphere and ensure it's printable
hollow_sphere = outer_sphere.difference(inner_sphere)
hollow_sphere.process(validate=True)

# Add a small support base for better printability
base = trimesh.creation.cylinder(radius=46, height=2)
hollow_sphere = hollow_sphere.union(base)

# Convert to numpy-stl format
vertices = hollow_sphere.vertices
faces = hollow_sphere.faces

numpy_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    numpy_mesh.vectors[i] = vertices[f]

# Save as binary STL (smaller file size)
numpy_mesh.save('hollow_sphere.stl')