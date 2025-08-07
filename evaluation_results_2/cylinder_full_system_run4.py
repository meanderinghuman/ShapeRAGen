import trimesh
import numpy as np

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40)

# Create inner cylinder (hollow part) with slightly smaller radius
inner_cylinder = trimesh.creation.cylinder(radius=14, height=40.1)  # Slightly taller to ensure clean boolean

# Create hollow cylinder by subtracting inner from outer
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure mesh is watertight (important for 3D printing)
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Export as STL file
hollow_cylinder.export('output.stl')