import trimesh
import numpy as np
from stl import mesh

# Create outer sphere with radius 45mm
outer_sphere = trimesh.creation.icosphere(radius=45, subdivisions=3)

# Create inner sphere with slightly smaller radius (44mm) to create 1mm wall thickness
inner_sphere = trimesh.creation.icosphere(radius=44, subdivisions=3)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and valid for 3D printing
hollow_sphere.process(validate=True)

# Export as STL file
hollow_sphere.export('output.stl')