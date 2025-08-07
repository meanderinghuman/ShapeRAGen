import trimesh
import numpy as np
from stl import mesh

# Define outer dimensions
outer_length = 30.0
outer_width = 20.0
outer_height = 40.0
wall_thickness = 2.0

# Calculate inner dimensions
inner_length = outer_length - 2 * wall_thickness
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - wall_thickness  # Only subtract from top, not bottom

# Create outer box
outer_box = trimesh.creation.box((outer_length, outer_width, outer_height))

# Create inner box (hollow space)
inner_box = trimesh.creation.box((inner_length, inner_width, inner_height))

# Position inner box (centered in x and y, flush with bottom in z)
inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight and valid for 3D printing
hollow_box.fill_holes()
hollow_box.fix_normals()

# Export as STL
hollow_box.export('output.stl')