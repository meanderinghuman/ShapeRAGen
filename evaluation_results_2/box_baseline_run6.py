import trimesh
import numpy as np
from stl import mesh

# Dimensions
base_x = 20.0  # mm
base_y = 30.0  # mm
height = 40.0  # mm
wall_thickness = 2.0  # mm

# Create outer box
outer_box = trimesh.primitives.Box(extents=[base_x, base_y, height])

# Create inner box (hollow space)
inner_x = base_x - 2 * wall_thickness
inner_y = base_y - 2 * wall_thickness
inner_z = height - wall_thickness  # Keep bottom solid
inner_box = trimesh.primitives.Box(extents=[inner_x, inner_y, inner_z])

# Position inner box centered within outer box
inner_box.apply_translation([0, 0, wall_thickness/2])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure mesh is watertight and valid for 3D printing
hollow_box.fill_holes()
hollow_box.process()

# Export as STL
hollow_box.export('output.stl')