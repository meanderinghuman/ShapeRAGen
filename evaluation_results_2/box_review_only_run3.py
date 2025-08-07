import trimesh
import numpy as np
from stl import mesh

# Define box dimensions (outer dimensions)
length = 30
width = 20
height = 40
wall_thickness = 2

# Create outer box
outer_box = trimesh.primitives.Box(extents=[length, width, height])

# Create inner box (hollow space)
inner_length = length - 2 * wall_thickness
inner_width = width - 2 * wall_thickness
inner_height = height - wall_thickness  # Only subtract from top to keep bottom solid
inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])

# Position inner box slightly above bottom to keep bottom solid
inner_box.apply_translation([0, 0, wall_thickness/2])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Export as STL
hollow_box.export('output.stl')