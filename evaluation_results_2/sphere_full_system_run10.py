import trimesh
import numpy as np
from stl import mesh

# Parameters
outer_radius = 45.0  # mm
wall_thickness = 1.0  # mm
support_height = 5.0  # mm
support_padding = 2.0  # mm

# Create outer sphere
outer_sphere = trimesh.creation.icosphere(radius=outer_radius, subdivisions=3)

# Create inner sphere with specified wall thickness
inner_radius = outer_radius - wall_thickness
if inner_radius <= 0:
    raise ValueError("Wall thickness cannot be larger than outer radius")
inner_sphere = trimesh.creation.icosphere(radius=inner_radius, subdivisions=3)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Process the mesh to ensure it's manifold and watertight
hollow_sphere = hollow_sphere.process(validate=True)

# Verify the mesh is suitable for printing
if not hollow_sphere.is_watertight:
    raise ValueError("Mesh is not watertight and cannot be 3D printed")
if not hollow_sphere.is_winding_consistent:
    hollow_sphere.fix_normals()

# Create a support structure (simple base plate)
support = trimesh.creation.box(extents=[2*outer_radius + 2*support_padding,
                                       2*outer_radius + 2*support_padding,
                                       support_height])
support.apply_translation([0, 0, -outer_radius - support_height/2])

# Combine the hollow sphere with its support
model = hollow_sphere + support

# Convert trimesh to numpy-stl mesh
vertices = model.vertices
faces = model.faces
numpy_stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        numpy_stl_mesh.vectors[i][j] = vertices[f[j], :]

# Save the STL file
numpy_stl_mesh.save('hollow_sphere_with_support.stl')