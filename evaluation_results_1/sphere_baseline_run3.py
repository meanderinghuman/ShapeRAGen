import trimesh
import numpy as np
from stl import mesh

# Create outer sphere
outer_sphere = trimesh.creation.icosphere(subdivisions=3, radius=45)

# Create inner sphere (hollow part)
inner_sphere = trimesh.creation.icosphere(subdivisions=3, radius=43)

# Combine to create hollow sphere
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and manifold
hollow_sphere.process()

# Export as STL
hollow_sphere.export('output.stl')