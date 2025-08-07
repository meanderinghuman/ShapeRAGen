import trimesh
import numpy as np
from stl import mesh

# Create outer sphere
outer_sphere = trimesh.creation.icosphere(subdivisions=3, radius=45)

# Create inner sphere (hollow space)
inner_sphere = trimesh.creation.icosphere(subdivisions=3, radius=43)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and valid for 3D printing
hollow_sphere.process()

# Export as STL file
hollow_sphere.export('output.stl')