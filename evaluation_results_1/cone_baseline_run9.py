import trimesh
import numpy as np

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius to create hollow space)
inner_cone = trimesh.creation.cone(radius=18, height=34)  # Slightly shorter to ensure watertight mesh

# Position inner cone slightly above base to ensure manifold mesh
inner_cone.apply_translation([0, 0, 1])

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and manifold
hollow_cone.fill_holes()
hollow_cone.process()

# Export as STL
hollow_cone.export('output.stl')