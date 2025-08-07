import trimesh
import numpy as np
from stl import mesh

# Parameters
outer_radius = 15.0  # mm
height = 40.0        # mm
wall_thickness = 2.0 # mm
inner_radius = outer_radius - wall_thickness

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=outer_radius, height=height)

# Create inner cylinder (to be subtracted)
inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=height)

# Subtract inner cylinder from outer cylinder to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure mesh is watertight for 3D printing
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Export as STL
hollow_cylinder.export('output.stl')