import trimesh
import numpy as np
from stl import mesh

# Create outer sphere (45mm radius)
outer_sphere = trimesh.creation.icosphere(radius=45.0)

# Create inner sphere (43.5mm radius for 1.5mm wall thickness)
inner_sphere = trimesh.creation.icosphere(radius=43.5)

# Create the hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight (important for 3D printing)
hollow_sphere.fill_holes()
hollow_sphere.process()

# Export as STL file
hollow_sphere.export('output.stl')