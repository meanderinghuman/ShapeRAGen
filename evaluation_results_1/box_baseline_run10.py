import trimesh
import numpy as np
from stl import mesh

# Outer dimensions
outer_length = 30
outer_width = 20
outer_height = 40

# Wall thickness (adjust as needed for printing)
wall_thickness = 2

# Create outer box
outer_box = trimesh.primitives.Box(extents=[outer_length, outer_width, outer_height])

# Create inner box (hollow space)
inner_box = trimesh.primitives.Box(extents=[
    outer_length - 2 * wall_thickness,
    outer_width - 2 * wall_thickness,
    outer_height - wall_thickness  # Keep bottom solid
])

# Position inner box (centered)
inner_box.apply_translation([0, 0, wall_thickness/2])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Export as STL
hollow_box.export('output.stl')