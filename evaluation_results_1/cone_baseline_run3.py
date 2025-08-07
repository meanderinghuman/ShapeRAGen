import trimesh
import numpy as np

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius to make it hollow)
inner_cone = trimesh.creation.cone(radius=18, height=34.5)  # Slightly shorter to ensure proper wall thickness

# Translate inner cone slightly up to create a base
inner_cone.apply_translation([0, 0, 0.5])

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight and valid for 3D printing
hollow_cone.process()
hollow_cone.fill_holes()

# Export as STL file
hollow_cone.export('output.stl')