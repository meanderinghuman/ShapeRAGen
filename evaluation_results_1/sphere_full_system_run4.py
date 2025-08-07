import trimesh
import numpy as np
from stl import mesh

# Create outer sphere (45mm radius)
outer_sphere = trimesh.creation.icosphere(radius=45.0)

# Create inner sphere (43.8mm radius for 1.2mm wall thickness)
inner_sphere = trimesh.creation.icosphere(radius=43.8)

# Create the hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Add a small vent hole (4mm diameter) to make it printable
vent_cylinder = trimesh.creation.cylinder(radius=2.0, height=100.0)
vent_cylinder.apply_translation([0, 0, -50])  # Center the cylinder
hollow_sphere = hollow_sphere.difference(vent_cylinder)

# Ensure the mesh is watertight and valid for printing
hollow_sphere.process(validate=True)
hollow_sphere.fill_holes()

# Convert to numpy-stl mesh and save
stl_mesh = mesh.Mesh(np.zeros(len(hollow_sphere.faces), dtype=mesh.Mesh.dtype))
stl_mesh.vectors = hollow_sphere.vertices[hollow_sphere.faces]
stl_mesh.save('output.stl')