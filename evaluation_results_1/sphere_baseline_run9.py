import trimesh
import numpy as np
from stl import mesh

# Create outer sphere
outer_sphere = trimesh.creation.icosphere(radius=45, subdivisions=3)

# Create inner sphere (hollow part)
inner_sphere = trimesh.creation.icosphere(radius=43, subdivisions=3)  # 45mm - 2mm thickness

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and correct normals
hollow_sphere.process()

# Export as STL
hollow_sphere.export('output.stl')