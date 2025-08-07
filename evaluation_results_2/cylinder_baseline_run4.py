import trimesh
import numpy as np

# Outer cylinder dimensions
outer_radius = 15.0
height = 40.0
wall_thickness = 2.0  # Recommended for FDM printing

# Create outer cylinder
outer_cylinder = trimesh.creation.cylinder(radius=outer_radius, height=height)

# Create inner cylinder (hollow part)
inner_radius = outer_radius - wall_thickness
inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=height)

# Subtract inner cylinder from outer cylinder to create hollow cylinder
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure the mesh is watertight and correct normals
hollow_cylinder.process()

# Export as STL file
hollow_cylinder.export('output.stl')