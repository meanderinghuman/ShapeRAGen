import trimesh
import numpy as np

# Create outer cylinder (radius 15mm, height 40mm)
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40)

# Create inner cylinder (radius 13mm, height 40mm to ensure complete hollowing)
inner_cylinder = trimesh.creation.cylinder(radius=13, height=40)

# Subtract inner cylinder from outer cylinder to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure the mesh is watertight and manifold for 3D printing
hollow_cylinder.process()

# Export as STL file
hollow_cylinder.export('output.stl')