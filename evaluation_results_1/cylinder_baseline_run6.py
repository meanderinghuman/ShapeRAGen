import trimesh
import numpy as np

# Create outer and inner cylinders
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40)
inner_cylinder = trimesh.creation.cylinder(radius=14, height=40.1)  # Slightly taller to ensure clean difference

# Position the inner cylinder (centered by default)
# Subtract inner from outer to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure the mesh is watertight and valid for printing
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Export as STL
hollow_cylinder.export('output.stl')