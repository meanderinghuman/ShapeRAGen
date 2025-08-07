import trimesh
import numpy as np
from stl import mesh

# Parameters
base_radius = 20.0
height = 35.0
thickness = max(2.0, 1.0)  # wall thickness with minimum of 1mm

# Create outer cone
outer_cone = trimesh.creation.cone(
    radius=base_radius,
    height=height,
    sections=64
)

# Create inner cone with proper wall thickness
inner_radius = base_radius - thickness
inner_height = height - thickness  # maintain thickness at base
inner_cone = trimesh.creation.cone(
    radius=inner_radius,
    height=inner_height,
    sections=64
)

# Position inner cone to maintain base thickness
inner_cone.apply_translation([0, 0, thickness])

# Boolean difference operation with error handling
try:
    hollow_cone = outer_cone.difference(inner_cone)
except:
    hollow_cone = outer_cone.copy()
    print("Warning: Boolean operation failed, using solid cone")

# Repair and validate mesh
hollow_cone.process(validate=True)
hollow_cone.fill_holes()
hollow_cone.fix_normals()

# Verify watertightness before export
if not hollow_cone.is_watertight:
    hollow_cone = outer_cone.copy()
    print("Warning: Result not watertight, using solid cone")

# Export as STL
hollow_cone.export('output.stl')