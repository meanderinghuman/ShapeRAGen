import trimesh
import numpy as np
from stl import mesh

# Create a hollow sphere (45mm radius, 2mm wall thickness)
sphere = trimesh.creation.icosphere(subdivisions=3, radius=45)
inner_sphere = trimesh.creation.icosphere(subdivisions=3, radius=43)
hollow_sphere = sphere.difference(inner_sphere)

# Ensure the mesh is watertight and valid for printing
hollow_sphere.fill_holes()
hollow_sphere.fix_normals()

# Export as STL
hollow_sphere.export('output.stl')