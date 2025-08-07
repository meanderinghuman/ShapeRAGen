import trimesh
import numpy as np

# Outer dimensions of the box
outer_length = 30.0  # x-dimension
outer_width = 20.0   # y-dimension
outer_height = 40.0  # z-dimension
wall_thickness = 2.0  # Recommended wall thickness for FDM printing

# Create outer box
outer_box = trimesh.primitives.Box(extents=[outer_length, outer_width, outer_height])

# Create inner box (hollow space)
inner_length = outer_length - 2 * wall_thickness
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - 2 * wall_thickness

# Ensure inner dimensions are positive
inner_length = max(inner_length, 0)
inner_width = max(inner_width, 0)
inner_height = max(inner_height, 0)

inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])

# Subtract inner box from outer box to create hollow box
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight (manifold) for 3D printing
hollow_box.fill_holes()
hollow_box.fix_normals()

# Export as STL file
hollow_box.export('output.stl')