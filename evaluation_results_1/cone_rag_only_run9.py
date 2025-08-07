import trimesh
import numpy as np
from stl import mesh as stl_mesh

# Create outer cone (larger radius)
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius to create hollow space)
inner_cone = trimesh.creation.cone(radius=18, height=34)  # Slightly shorter to ensure watertight mesh

# Position the inner cone slightly inside the outer cone
inner_cone.apply_translation([0, 0, 0.5])  # Move up 0.5mm to create bottom thickness

# Create the hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight and manifold
hollow_cone.process()

# Add a small hole at the top to prevent vacuum during printing
top_hole = trimesh.creation.cylinder(radius=2, height=5)
top_hole.apply_translation([0, 0, 35])  # Position at top of cone
hollow_cone = hollow_cone.union(top_hole)

# Export as STL
hollow_cone.export('output.stl')