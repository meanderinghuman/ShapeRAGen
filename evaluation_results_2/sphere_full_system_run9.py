import trimesh
import numpy as np
from stl import mesh

# Create spheres with specified wall thickness
outer_radius = 45.0
wall_thickness = 1.2
inner_radius = outer_radius - wall_thickness

outer_sphere = trimesh.creation.icosphere(radius=outer_radius)
inner_sphere = trimesh.creation.icosphere(radius=inner_radius)

# Create hollow sphere and ensure manifold
hollow_sphere = outer_sphere.difference(inner_sphere)
hollow_sphere.fill_holes()
hollow_sphere.process()

# Convert to numpy-stl mesh using more efficient method
vertices = hollow_sphere.vertices
faces = hollow_sphere.faces
data = np.zeros(len(faces), dtype=mesh.Mesh.dtype)
data['vectors'] = vertices[faces]
stl_mesh = mesh.Mesh(data)

# Save as binary STL (smaller file size)
stl_mesh.save('hollow_sphere.stl')