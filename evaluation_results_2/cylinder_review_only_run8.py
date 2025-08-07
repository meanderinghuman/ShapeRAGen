import trimesh
import numpy as np
from stl import mesh

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40)

# Create inner cylinder (hollow part) with slightly smaller radius
inner_cylinder = trimesh.creation.cylinder(radius=13, height=40.1)  # Slightly taller to ensure clean boolean

# Perform boolean difference to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure the mesh is watertight and valid for 3D printing
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Export as STL file
hollow_cylinder.export('output.stl')