import trimesh
import numpy as np

# Create a hollow sphere (outer radius 45mm, inner radius 43mm)
outer_sphere = trimesh.creation.icosphere(radius=45, subdivisions=3)
inner_sphere = trimesh.creation.icosphere(radius=43, subdivisions=3)

# Create the hollow mesh by subtracting the inner sphere from the outer
hollow_sphere = outer_sphere.difference(inner_sphere)

# Ensure the mesh is watertight (important for 3D printing)
hollow_sphere.fill_holes()
hollow_sphere.process()

# Export as STL file
hollow_sphere.export('output.stl')