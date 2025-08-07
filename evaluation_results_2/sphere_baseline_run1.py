import trimesh
import numpy as np

# Create outer sphere (radius 45mm)
outer_sphere = trimesh.creation.icosphere(radius=45, subdivisions=3)

# Create inner sphere (radius 43mm for 2mm wall thickness)
inner_sphere = trimesh.creation.icosphere(radius=43, subdivisions=3)

# Create hollow sphere by subtracting inner from outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight and valid for 3D printing
hollow_sphere.process()

# Export as STL file
hollow_sphere.export('output.stl')