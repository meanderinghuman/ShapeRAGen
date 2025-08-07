import trimesh
import numpy as np
from stl import mesh

# Create outer sphere (45mm radius)
outer_sphere = trimesh.creation.icosphere(subdivisions=3, radius=45.0)

# Create inner sphere (43.5mm radius for 1.5mm wall thickness)
inner_sphere = trimesh.creation.icosphere(subdivisions=3, radius=43.5)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and valid for 3D printing
hollow_sphere.fill_holes()
hollow_sphere.fix_normals()

# Export as binary STL
hollow_sphere.export('output.stl', file_type='stl')