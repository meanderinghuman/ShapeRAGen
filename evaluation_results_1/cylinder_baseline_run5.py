import trimesh
import numpy as np

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40)

# Create inner cylinder (hollow part)
inner_cylinder = trimesh.creation.cylinder(radius=12, height=40)

# Subtract inner cylinder from outer cylinder to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Export as STL file
hollow_cylinder.export('output.stl')