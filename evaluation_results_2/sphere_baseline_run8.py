import trimesh
import numpy as np
from stl import mesh

# Create outer sphere
outer_sphere = trimesh.creation.icosphere(radius=45, subdivisions=3)

# Create inner sphere (hollow part)
inner_sphere = trimesh.creation.icosphere(radius=43, subdivisions=3)  # 45 - 2 = 43mm radius for 2mm wall thickness

# Create the hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and valid for 3D printing
hollow_sphere = hollow_sphere.process()

# Export as STL
hollow_sphere.export('output.stl')