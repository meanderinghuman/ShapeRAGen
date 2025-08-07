import trimesh
import numpy as np
from stl import mesh

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40)

# Create inner cylinder (with slightly smaller radius to make it hollow)
inner_cylinder = trimesh.creation.cylinder(radius=14, height=40)

# Subtract inner cylinder from outer to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure the mesh is watertight and valid for printing
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Export as STL file
hollow_cylinder.export('output.stl')