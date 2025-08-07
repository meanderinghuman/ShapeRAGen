import trimesh
import numpy as np
from stl import mesh

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=15, height=40)

# Create inner cylinder (hollow part)
inner_cylinder = trimesh.creation.cylinder(radius=14, height=40.1)  # Slightly taller to ensure clean boolean

# Position inner cylinder exactly centered
inner_cylinder.apply_translation([0, 0, -0.05])  # Adjust for the extra height

# Create hollow cylinder by difference
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure mesh is watertight and correct normals
hollow_cylinder.process()

# Export as STL
hollow_cylinder.export('output.stl')