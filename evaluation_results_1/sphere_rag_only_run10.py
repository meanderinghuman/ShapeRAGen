import trimesh
import numpy as np
from stl import mesh

# Create outer sphere (45mm radius)
outer_sphere = trimesh.creation.icosphere(radius=45, subdivisions=4)

# Create inner sphere (44mm radius for 1mm wall thickness)
inner_sphere = trimesh.creation.icosphere(radius=44, subdivisions=4)

# Combine to create hollow sphere
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure mesh is watertight and manifold for printing
hollow_sphere.fill_holes()
hollow_sphere.process()

# Export as STL file
hollow_sphere.export('output.stl')