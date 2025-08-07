import trimesh
import numpy as np

# Create outer box dimensions with units
outer_length_mm = 30.0
outer_width_mm = 20.0
outer_height_mm = 40.0
min_wall_thickness_mm = 1.2  # Minimum recommended for FDM printing

# Calculate inner box dimensions
inner_length_mm = outer_length_mm - 2 * min_wall_thickness_mm
inner_width_mm = outer_width_mm - 2 * min_wall_thickness_mm
inner_height_mm = outer_height_mm - 2 * min_wall_thickness_mm

# Validate dimensions
if (inner_length_mm <= 0 or inner_width_mm <= 0 or inner_height_mm <= 0):
    raise ValueError("Wall thickness results in negative inner dimensions")

# Create outer box
outer_box = trimesh.creation.box(extents=[outer_length_mm, outer_width_mm, outer_height_mm])

# Create inner box (hollow space)
inner_box = trimesh.creation.box(extents=[inner_length_mm, inner_width_mm, inner_height_mm])

# Position inner box at center
inner_box.apply_translation([min_wall_thickness_mm, min_wall_thickness_mm, min_wall_thickness_mm])

# Subtract inner box from outer box to create hollow box
hollow_box = outer_box.difference(inner_box)

# Process and validate mesh
hollow_box = hollow_box.process()
if not hollow_box.is_watertight:
    raise ValueError("Resulting mesh is not watertight - not suitable for 3D printing")

# Export as STL
hollow_box.export('output.stl')