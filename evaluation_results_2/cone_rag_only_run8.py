import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (smaller radius to make it hollow)
inner_cone = trimesh.creation.cone(radius=18, height=35)  # 2mm wall thickness

# Subtract inner cone from outer cone to create hollow cone
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight and valid for 3D printing
hollow_cone.process(validate=True)
hollow_cone.fill_holes()

# Export as STL
hollow_cone.export('output.stl')