import trimesh
import numpy as np

# Create outer cylinder
outer_radius = 15.0
height = 40.0
outer_cylinder = trimesh.creation.cylinder(radius=outer_radius, height=height)

# Create inner cylinder (hollow part)
wall_thickness = 2.0  # Standard FDM wall thickness
inner_radius = outer_radius - wall_thickness
inner_cylinder = trimesh.creation.cylinder(radius=inner_radius, height=height)

# Subtract inner cylinder from outer cylinder to create hollow shape
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Ensure the mesh is watertight and suitable for printing
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Export as STL file
hollow_cylinder.export('output.stl')