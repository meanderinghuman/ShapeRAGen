import trimesh
import numpy as np
from stl import mesh

# Create outer sphere
outer_sphere = trimesh.creation.icosphere(radius=45)

# Create inner sphere (hollow space)
inner_sphere = trimesh.creation.icosphere(radius=43)  # 2mm wall thickness

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Export as STL
hollow_sphere.export('output.stl')