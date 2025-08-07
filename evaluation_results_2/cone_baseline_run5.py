import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius to make it hollow)
inner_cone = trimesh.creation.cone(radius=18, height=34)  # Slightly shorter to ensure proper hollowing

# Position the inner cone slightly inside the outer cone
inner_cone.apply_translation([0, 0, 0.5])  # Move up slightly to create bottom thickness

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight and suitable for printing
hollow_cone.fill_holes()
hollow_cone.fix_normals()

# Export as STL
hollow_cone.export('output.stl')