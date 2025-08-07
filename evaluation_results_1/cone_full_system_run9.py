import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius for hollow effect)
inner_cone = trimesh.creation.cone(radius=18, height=35)

# Subtract inner cone from outer cone to create hollow cone
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and suitable for printing
hollow_cone.fill_holes()
hollow_cone.update_faces(hollow_cone.nondegenerate_faces())
hollow_cone.update_faces(hollow_cone.unique_faces())
hollow_cone.remove_unreferenced_vertices()

# Export as STL file
hollow_cone.export('output.stl')