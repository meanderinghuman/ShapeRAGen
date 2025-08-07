import trimesh
import numpy as np
from stl import mesh

# Create outer pyramid (larger dimensions)
outer_base = 25.0  # mm
outer_height = 30.0  # mm
outer_pyramid = trimesh.creation.cone(radius=outer_base/2, height=outer_height, sections=4)

# Create inner pyramid (smaller dimensions to create hollow space)
wall_thickness = 2.0  # mm
inner_base = outer_base - (2 * wall_thickness)
inner_height = outer_height - wall_thickness
inner_pyramid = trimesh.creation.cone(radius=inner_base/2, height=inner_height, sections=4)

# Position the inner pyramid slightly above the base to create a solid bottom
inner_pyramid.apply_translation([0, 0, wall_thickness])

# Create the hollow pyramid by subtracting inner from outer
hollow_pyramid = outer_pyramid.difference(inner_pyramid)

# Ensure the mesh is watertight and valid for 3D printing
hollow_pyramid.process(validate=True)
hollow_pyramid.fill_holes()

# Export as STL file
hollow_pyramid.export('output.stl')