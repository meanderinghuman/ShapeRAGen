import trimesh
import numpy as np
from stl import mesh

# Create outer box dimensions
outer_length = 30  # x-axis
outer_width = 20   # y-axis
outer_height = 40  # z-axis
wall_thickness = 1.2  # Recommended minimum for FDM printing

# Create inner box dimensions (hollow)
inner_length = outer_length - 2 * wall_thickness
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - 2 * wall_thickness

# Create outer and inner boxes
outer_box = trimesh.primitives.Box(extents=[outer_length, outer_width, outer_height])
inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])

# Subtract inner box from outer box to create hollow box
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight (important for 3D printing)
hollow_box.fill_holes()
hollow_box.process()

# Export as STL
hollow_box.export('output.stl')