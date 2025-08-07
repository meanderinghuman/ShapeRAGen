import trimesh
import numpy as np
from stl import mesh

# Create outer cone (larger radius)
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius to make it hollow)
inner_cone = trimesh.creation.cone(radius=18, height=34)  # Slightly shorter to ensure proper top closure

# Position the inner cone slightly inside the outer cone
inner_cone.apply_translation([0, 0, 0.5])  # Move up slightly to ensure wall thickness at bottom

# Subtract inner cone from outer cone to create hollow cone
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and manifold for printing
hollow_cone.fill_holes()
hollow_cone.process()

# Add a small base plate for better printing
base = trimesh.creation.cylinder(radius=20, height=1)
hollow_cone = hollow_cone.union(base)

# Export as STL
hollow_cone.export('output.stl')