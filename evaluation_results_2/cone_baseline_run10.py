import trimesh
import numpy as np

# Parameters
base_radius = 20.0
height = 35.0
thickness = 1.0  # wall thickness for FDM printing

# Create outer cone
outer_cone = trimesh.creation.cone(radius=base_radius, height=height)

# Create inner cone (smaller radius to create hollow space)
inner_radius = base_radius - thickness
inner_cone = trimesh.creation.cone(radius=inner_radius, height=height-thickness)

# Position the inner cone slightly above the base to create a solid bottom
inner_cone.apply_translation([0, 0, thickness])

# Subtract inner cone from outer cone to create hollow shape
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight and valid for 3D printing
hollow_cone.process()

# Export as STL
hollow_cone.export('output.stl')