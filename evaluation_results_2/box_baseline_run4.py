import trimesh
import numpy as np
from stl import mesh

# Define outer and inner dimensions
outer_width = 30
outer_length = 20
outer_height = 40
wall_thickness = 2  # Recommended for FDM printing

# Calculate inner dimensions
inner_width = outer_width - 2 * wall_thickness
inner_length = outer_length - 2 * wall_thickness
inner_height = outer_height - wall_thickness  # Keep bottom solid

# Create outer box
outer_box = trimesh.primitives.Box(extents=[outer_width, outer_length, outer_height])

# Create inner box (hollow space)
inner_box = trimesh.primitives.Box(extents=[inner_width, inner_length, inner_height])

# Position inner box centered within outer box
inner_box.apply_translation([0, 0, wall_thickness / 2])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure mesh is watertight and valid for 3D printing
hollow_box.fill_holes()
hollow_box.fix_normals()

# Export as STL
hollow_box.export('output.stl')