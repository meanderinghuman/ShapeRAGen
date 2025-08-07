import trimesh
import numpy as np
from stl import mesh

# Parameters
base_radius = 20.0
height = 35.0
wall_thickness = 1.0
segments = 64  # Number of segments for the circular base

# Create outer cone
outer_cone = trimesh.creation.cone(radius=base_radius, height=height, sections=segments)

# Create inner cone (smaller radius to create hollow space)
inner_radius = base_radius - wall_thickness
inner_cone = trimesh.creation.cone(radius=inner_radius, height=height-wall_thickness, sections=segments)

# Position inner cone slightly above base to create bottom surface
inner_cone.apply_translation([0, 0, wall_thickness])

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Ensure mesh is watertight and correct normals
hollow_cone.fill_holes()
hollow_cone.fix_normals()

# Export as STL
hollow_cone.export('output.stl')