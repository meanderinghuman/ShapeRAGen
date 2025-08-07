import trimesh
import numpy as np
from stl import mesh as stl_mesh

# Create a hollow sphere
radius = 45.0
thickness = 2.0  # Wall thickness in mm

# Create outer sphere
outer_sphere = trimesh.creation.icosphere(radius=radius)

# Create inner sphere (hollow part)
inner_sphere = trimesh.creation.icosphere(radius=radius - thickness)

# Create the hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and valid for printing
hollow_sphere = hollow_sphere.process(validate=True)

# Export as STL
hollow_sphere.export('output.stl')