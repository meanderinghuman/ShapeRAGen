import trimesh
import numpy as np
from stl import mesh

# Create outer sphere (radius 45mm)
outer_sphere = trimesh.creation.icosphere(subdivisions=3, radius=45.0)

# Create inner sphere (radius 44mm to make 1mm wall thickness)
inner_sphere = trimesh.creation.icosphere(subdivisions=3, radius=44.0)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight (manifold) for 3D printing
hollow_sphere.fill_holes()
hollow_sphere.process()

# Export as STL file
hollow_sphere.export('output.stl')