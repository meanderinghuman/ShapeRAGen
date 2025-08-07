import trimesh
import numpy as np
from stl import mesh as stl_mesh

# Create outer and inner spheres
outer_sphere = trimesh.creation.icosphere(subdivisions=3, radius=45)
inner_sphere = trimesh.creation.icosphere(subdivisions=3, radius=43)

# Create the hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and valid for 3D printing
hollow_sphere.process()
hollow_sphere.fill_holes()
hollow_sphere.fix_normals()

# Export as STL
hollow_sphere.export('output.stl')