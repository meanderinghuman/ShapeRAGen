import trimesh
import numpy as np
from stl import mesh

# Create outer cone with print-friendly dimensions
outer_cone = trimesh.creation.cone(radius=20, height=35)

# Create inner cone with proper wall thickness (2mm) and height clearance
inner_cone = trimesh.creation.cone(radius=18, height=33)

# Subtract inner cone from outer cone to create hollow cone
hollow_cone = outer_cone.difference(inner_cone)

# Process and validate mesh
hollow_cone.fill_holes()
hollow_cone.process()
assert hollow_cone.is_watertight, "Mesh is not watertight"
assert hollow_cone.is_winding_consistent, "Mesh has inconsistent winding"
assert hollow_cone.is_volume, "Mesh is not a solid volume"

# Add a small base for better print adhesion
base = trimesh.creation.cylinder(radius=20, height=1)
hollow_cone = hollow_cone.union(base)

# Export as STL file
hollow_cone.export('output.stl')