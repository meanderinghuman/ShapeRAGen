import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid (base 25x25mm, height 30mm)
outer_pyramid = trimesh.creation.cone(radius=12.5, height=30, sections=4)

# Create inner pyramid (smaller dimensions to make it hollow)
wall_thickness = 1.2  # Standard FDM wall thickness
inner_radius = 12.5 - wall_thickness
inner_height = 30 - wall_thickness
inner_pyramid = trimesh.creation.cone(radius=inner_radius, height=inner_height, sections=4)

# Position the inner pyramid slightly above the base to create a floor
inner_pyramid.apply_translation([0, 0, wall_thickness])

# Create the hollow pyramid by subtracting inner from outer
hollow_pyramid = outer_pyramid.difference(inner_pyramid)

# Ensure the mesh is watertight and valid for 3D printing
hollow_pyramid.fill_holes()
hollow_pyramid.process()

# Export as STL file
hollow_pyramid.export('output.stl')