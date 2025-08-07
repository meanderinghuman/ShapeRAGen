import trimesh
import numpy as np
from stl import mesh

# Define outer dimensions
outer_length = 30
outer_width = 20
outer_height = 40

# Define wall thickness
wall_thickness = 2

# Create outer box
outer_box = trimesh.primitives.Box(extents=[outer_length, outer_width, outer_height])

# Create inner box dimensions
inner_length = outer_length - 2 * wall_thickness
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - wall_thickness  # Only subtract from top to keep bottom solid

# Create inner box
inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])

# Position inner box centered within outer box
inner_box.apply_translation([0, 0, wall_thickness/2])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Export as STL
hollow_box.export('output.stl')