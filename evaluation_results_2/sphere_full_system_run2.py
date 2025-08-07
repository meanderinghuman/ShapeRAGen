import trimesh
import numpy as np
from stl import mesh

# Create outer sphere with 45mm radius
outer_sphere = trimesh.creation.icosphere(radius=45)

# Create inner sphere with slightly smaller radius (44mm) to create 1mm wall thickness
inner_sphere = trimesh.creation.icosphere(radius=44)

# Create the hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and manifold for printing
hollow_sphere.fill_holes()
hollow_sphere.process()

# Export as binary STL file
hollow_sphere.export('output.stl', file_type='stl')