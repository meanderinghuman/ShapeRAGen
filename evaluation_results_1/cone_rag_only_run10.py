import trimesh
import numpy as np
from stl import mesh as stl_mesh

# Parameters
outer_radius = 20.0  # mm
height = 35.0        # mm
wall_thickness = 2.0 # mm
inner_radius = outer_radius - wall_thickness

# Create outer cone
outer_cone = trimesh.creation.cone(radius=outer_radius, height=height)

# Create inner cone (smaller radius to make it hollow)
inner_cone = trimesh.creation.cone(radius=inner_radius, height=height)

# Create base circle for better printability
base_outer = trimesh.creation.cylinder(radius=outer_radius, height=wall_thickness)
base_inner = trimesh.creation.cylinder(radius=inner_radius, height=wall_thickness)

# Position the base at the bottom of the cone
base_outer.apply_translation([0, 0, -wall_thickness])
base_inner.apply_translation([0, 0, -wall_thickness])

# Subtract inner cone from outer cone to create hollow space
hollow_cone = outer_cone.difference(inner_cone)

# Subtract inner base from outer base
solid_base = base_outer.difference(base_inner)

# Combine the hollow cone with the solid base
final_mesh = hollow_cone + solid_base

# Ensure the mesh is watertight and valid for printing
final_mesh.process()

# Export as STL file
final_mesh.export('output.stl')