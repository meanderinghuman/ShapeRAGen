import trimesh
import numpy as np
from stl import mesh

# Parameters
base_radius = 20.0
height = 35.0
wall_thickness = 2.0  # Minimum recommended for FDM printing
base_thickness = 2.0  # Added base for stability
resolution = 50  # Higher resolution for smoother curves

# Create outer cone
outer_cone = trimesh.creation.cone(
    radius=base_radius,
    height=height,
    sections=resolution
)

# Create inner cone (hollow space)
inner_radius = base_radius - wall_thickness
inner_cone = trimesh.creation.cone(
    radius=inner_radius,
    height=height,
    sections=resolution
)

# Create base plate
base_cylinder = trimesh.creation.cylinder(
    radius=base_radius,
    height=base_thickness
)

# Subtract inner cone from outer cone to create hollow cone
hollow_cone = outer_cone.difference(inner_cone)

# Combine with base plate
final_mesh = hollow_cone.union(base_cylinder)

# Process mesh
final_mesh.process()
if not final_mesh.is_watertight:
    final_mesh.fill_holes()
    final_mesh.process()

# Export
final_mesh.export('output.stl')