import trimesh
import numpy as np
from stl import mesh as stl_mesh

# Create outer cone
outer_radius = 20.0
height = 35.0
outer_cone = trimesh.creation.cone(radius=outer_radius, height=height)

# Create inner cone (hollow space)
wall_thickness = 2.0  # Recommended for FDM printing
inner_radius = outer_radius - wall_thickness
inner_cone = trimesh.creation.cone(radius=inner_radius, height=height)

# Translate inner cone slightly to ensure proper boolean operation
inner_cone.apply_translation([0, 0, 0.1])

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and valid for 3D printing
hollow_cone.process(validate=True)
hollow_cone.fill_holes()

# Export as STL
hollow_cone.export('output.stl')