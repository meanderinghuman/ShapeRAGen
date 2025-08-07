import trimesh
import numpy as np
from stl import mesh

# Parameters
outer_radius = 15.0  # mm
inner_radius = 13.0  # mm (2mm wall thickness)
height = 40.0        # mm

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=outer_radius, height=height)

# Create inner cylinder (to be subtracted)
inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=height * 1.1)  # Slightly taller to ensure clean subtraction

# Subtract inner cylinder from outer cylinder to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure the mesh is watertight and valid for 3D printing
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Export as STL
hollow_cylinder.export('output.stl')