import trimesh
import numpy as np
from stl import mesh

# Parameters
base_radius = 20.0
height = 35.0
thickness = 2.0  # Wall thickness for FDM printing
segments = 64    # Number of segments for the circular base

# Create outer cone
outer_cone = trimesh.creation.cone(radius=base_radius, height=height, sections=segments)

# Create inner cone (smaller radius to make it hollow)
inner_radius = base_radius - thickness
inner_cone = trimesh.creation.cone(radius=inner_radius, height=height, sections=segments)

# Subtract inner cone from outer cone to create hollow cone
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight and correct normals
hollow_cone.process()
hollow_cone.fill_holes()
hollow_cone.fix_normals()

# Export as STL
hollow_cone.export('output.stl')