import trimesh
import numpy as np
from stl import mesh

# Create outer sphere (45mm radius)
outer_sphere = trimesh.creation.icosphere(radius=45)

# Create inner sphere (44mm radius to make 1mm wall thickness)
inner_sphere = trimesh.creation.icosphere(radius=44)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight (important for 3D printing)
hollow_sphere = hollow_sphere.process(validate=True)

# Export as STL file
hollow_sphere.export('output.stl')