import trimesh
import numpy as np
from stl import mesh

# Create a hollow sphere
radius = 45.0
thickness = 2.0

# Create outer and inner spheres
outer_sphere = trimesh.creation.icosphere(radius=radius)
inner_sphere = trimesh.creation.icosphere(radius=radius - thickness)

# Create the hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and manifold
hollow_sphere.process()

# Export as STL
hollow_sphere.export('output.stl')