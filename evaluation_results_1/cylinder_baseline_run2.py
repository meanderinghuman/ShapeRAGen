import trimesh
import numpy as np
from stl import mesh

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40)

# Create inner cylinder (hollow part) with slightly smaller radius
inner_cylinder = trimesh.creation.cylinder(radius=14, height=40.1)  # Slightly taller to ensure clean boolean

# Subtract inner cylinder from outer cylinder to create hollow shape
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure mesh is watertight and suitable for 3D printing
hollow_cylinder.fill_holes()
hollow_cylinder.fix_normals()

# Export as STL
hollow_cylinder.export('output.stl')