import trimesh
import numpy as np
from stl import mesh

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40)

# Create inner cylinder (smaller radius to create hollow space)
inner_cylinder = trimesh.creation.cylinder(radius=14, height=40)  # 1mm wall thickness

# Subtract inner cylinder from outer to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure the mesh is watertight (important for 3D printing)
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Export as STL file
hollow_cylinder.export('output.stl')