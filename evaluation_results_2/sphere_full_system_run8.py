import trimesh
import numpy as np
from stl import mesh

# Create outer sphere (45mm radius)
outer_sphere = trimesh.creation.icosphere(radius=45)

# Create inner sphere (43mm radius for 2mm wall thickness)
inner_sphere = trimesh.creation.icosphere(radius=43)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and manifold
hollow_sphere.process()

# Export as STL file
hollow_sphere.export('output.stl')