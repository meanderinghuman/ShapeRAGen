import trimesh
import numpy as np
from stl import mesh

# Parameters
radius = 15.0  # mm
height = 40.0  # mm
wall_thickness = 2.0  # mm

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=radius, height=height)

# Create inner cylinder (for hollow space)
inner_radius = radius - wall_thickness
inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=height)

# Subtract inner cylinder from outer cylinder to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure the mesh is watertight (important for 3D printing)
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Export as STL
hollow_cylinder.export('output.stl')