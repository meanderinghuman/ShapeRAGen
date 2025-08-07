import trimesh
import numpy as np
from stl import mesh

# Create outer sphere
outer_sphere = trimesh.creation.icosphere(radius=45, subdivisions=3)

# Create inner sphere (hollow part) with 2mm wall thickness
inner_sphere = trimesh.creation.icosphere(radius=43, subdivisions=3)

# Create the hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and correct normals
hollow_sphere.fill_holes()
hollow_sphere.fix_normals()

# Export as STL
hollow_sphere.export('output.stl')