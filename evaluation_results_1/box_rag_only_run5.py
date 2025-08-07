import trimesh
import numpy as np

# Define outer dimensions (mm)
outer_length = 30  # x dimension
outer_width = 20   # y dimension
outer_height = 40  # z dimension
wall_thickness = 1.2  # recommended for FDM printing

# Create outer box
outer_box = trimesh.creation.box(extents=[outer_length, outer_width, outer_height])

# Calculate inner dimensions (subtracting wall thickness from both sides)
inner_length = outer_length - 2 * wall_thickness
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - 2 * wall_thickness

# Create inner box (hollow space)
inner_box = trimesh.creation.box(extents=[inner_length, inner_width, inner_height])

# Subtract inner box from outer box to create hollow box
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight and valid for 3D printing
hollow_box.fill_holes()
hollow_box.fix_normals()

# Export as STL file
hollow_box.export('output.stl')