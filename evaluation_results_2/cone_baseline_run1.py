import trimesh
import numpy as np
from stl import mesh

# Parameters
base_radius = 20.0  # mm
height = 35.0       # mm
wall_thickness = 1.0  # mm

# Create outer cone
outer_cone = trimesh.creation.cone(radius=base_radius, height=height)

# Create inner cone (hollow part)
inner_radius = base_radius - wall_thickness
inner_height = height - wall_thickness  # Slightly shorter to maintain thickness at top
inner_cone = trimesh.creation.cone(radius=inner_radius, height=inner_height)

# Position inner cone slightly above base to maintain thickness
inner_cone.apply_translation([0, 0, wall_thickness])

# Create hollow cone by subtracting inner from outer
hollow_cone = outer_cone.difference(inner_cone)

# Export as STL
hollow_cone.export('output.stl')