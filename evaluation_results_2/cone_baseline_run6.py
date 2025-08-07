import trimesh
import numpy as np

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius to make it hollow)
inner_cone = trimesh.creation.cone(radius=18, height=34.5)

# Position inner cone slightly inside outer cone
inner_cone.apply_translation([0, 0, 0.25])

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and valid for 3D printing
hollow_cone.process()

# Export as STL file
hollow_cone.export('output.stl')