import trimesh
import numpy as np

# Parameters
radius = 15.0
height = 40.0
thickness = 2.0

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=radius, height=height)

# Create inner cylinder (hollow part)
inner_radius = radius - thickness
inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=height)

# Subtract inner from outer to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Export as STL
hollow_cylinder.export('output.stl')