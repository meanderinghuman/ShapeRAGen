import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius to make it hollow)
inner_cone = trimesh.creation.cone(radius=18, height=34)

# Subtract inner cone from outer cone to create hollow cone
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight and suitable for printing
hollow_cone.fill_holes()
hollow_cone = hollow_cone.process()

# Export as STL
hollow_cone.export('output.stl')