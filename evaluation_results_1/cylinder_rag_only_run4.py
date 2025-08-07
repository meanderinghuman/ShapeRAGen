import trimesh
import numpy as np

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40)

# Create inner cylinder (with smaller radius to make it hollow)
inner_radius = 15 - 2  # 2mm wall thickness
inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=40)

# Subtract inner cylinder from outer cylinder to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure the mesh is watertight (important for 3D printing)
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Export as STL file
hollow_cylinder.export('output.stl')