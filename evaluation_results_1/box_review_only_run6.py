import trimesh
import numpy as np
from stl import mesh

# Define outer dimensions
outer_length = 30
outer_width = 20
outer_height = 40

# Define wall thickness
thickness = 2

# Create outer box
outer_box = trimesh.creation.box((outer_length, outer_width, outer_height))

# Create inner box dimensions
inner_length = outer_length - 2 * thickness
inner_width = outer_width - 2 * thickness
inner_height = outer_height - thickness  # Only remove thickness from top to keep bottom solid

# Create inner box
inner_box = trimesh.creation.box((inner_length, inner_width, inner_height))

# Position inner box to create hollow space
inner_box.apply_translation((thickness, thickness, thickness))

# Subtract inner box from outer box to create hollow
hollow_box = outer_box.difference(inner_box)

# Export as STL
hollow_box.export('output.stl')