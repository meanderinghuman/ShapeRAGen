import trimesh
import numpy as np
from stl import mesh

# Create outer cone
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone (slightly smaller to create hollow space)
inner_cone = trimesh.creation.cone(radius=18, height=34)

# Subtract inner cone from outer cone to create hollow cone
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight and manifold for printing
hollow_cone.process()

# Export as STL file
hollow_cone.export('output.stl')