import trimesh
import numpy as np

# Outer dimensions of the box
outer_length = 30
outer_width = 20
outer_height = 40

# Wall thickness (adjust as needed for FDM printing)
wall_thickness = 2.0

# Create outer box
outer_box = trimesh.creation.box((outer_length, outer_width, outer_height))

# Calculate inner dimensions
inner_length = outer_length - 2 * wall_thickness
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - wall_thickness  # Keep bottom solid

# Create inner box (hollow space)
inner_box = trimesh.creation.box((inner_length, inner_width, inner_height))

# Position inner box centered within outer box
inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Export as STL
hollow_box.export('output.stl')