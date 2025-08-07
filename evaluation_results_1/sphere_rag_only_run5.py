import trimesh
import numpy as np
from stl import mesh

# Create outer sphere (45mm radius)
outer_sphere = trimesh.creation.icosphere(radius=45.0, subdivisions=4)

# Create inner sphere (43.8mm radius for 1.2mm wall thickness)
inner_sphere = trimesh.creation.icosphere(radius=43.8, subdivisions=4)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight (manifold)
hollow_sphere.fill_holes()
hollow_sphere.process()

# Export as STL file
hollow_sphere.export('output.stl')