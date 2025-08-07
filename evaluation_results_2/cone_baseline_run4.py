import trimesh
import numpy as np
from stl import mesh as stl_mesh

# Parameters
base_radius = 20.0
height = 35.0
thickness = 2.0  # wall thickness for FDM printing
resolution = 100  # number of segments in the base circle

# Create outer cone
outer_cone = trimesh.creation.cone(radius=base_radius, height=height, sections=resolution)

# Create inner cone (smaller radius to create hollow space)
inner_radius = base_radius - thickness
inner_cone = trimesh.creation.cone(radius=inner_radius, height=height-thickness, sections=resolution)

# Move inner cone up slightly to create base floor
inner_cone.apply_translation([0, 0, thickness])

# Combine the meshes to create a hollow cone
hollow_cone = outer_cone.difference(inner_cone)

# Ensure the mesh is watertight and valid for printing
hollow_cone.process()

# Export as STL
hollow_cone.export('output.stl')