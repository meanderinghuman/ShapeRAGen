import trimesh
import numpy as np

# Outer dimensions of the box
outer_length = 30
outer_width = 20
outer_height = 40

# Wall thickness
wall_thickness = 1

# Create outer box
outer_box = trimesh.creation.box((outer_length, outer_width, outer_height))

# Calculate inner dimensions
inner_length = outer_length - 2 * wall_thickness
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - wall_thickness  # Only subtract from top to keep bottom solid

# Create inner box (will be subtracted)
inner_box = trimesh.creation.box((inner_length, inner_width, inner_height))

# Position the inner box correctly (centered in x and y, flush with bottom)
inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Export as STL
hollow_box.export('output.stl')