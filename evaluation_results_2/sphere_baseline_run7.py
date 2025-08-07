import trimesh
import numpy as np
from stl import mesh

# Create outer sphere
outer_sphere = trimesh.creation.icosphere(subdivisions=3, radius=45)

# Create inner sphere (smaller radius for hollow effect)
inner_sphere = trimesh.creation.icosphere(subdivisions=3, radius=43)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and correct normals
hollow_sphere.process()

# Export as STL
hollow_sphere.export('output.stl')