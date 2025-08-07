import trimesh
import numpy as np

# Create outer sphere
outer_sphere = trimesh.creation.icosphere(radius=45, subdivisions=3)

# Create inner sphere (hollow part) with 2mm wall thickness
inner_sphere = trimesh.creation.icosphere(radius=43, subdivisions=3)

# Create the hollow sphere by subtracting the inner sphere from the outer sphere
hollow_sphere = outer_sphere.difference(inner_sphere)

# Export the hollow sphere as STL file
hollow_sphere.export('output.stl')