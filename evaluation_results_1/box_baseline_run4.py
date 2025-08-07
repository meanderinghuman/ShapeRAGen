import trimesh
import numpy as np
from stl import mesh

# Create outer box dimensions
outer_length = 30  # mm
outer_width = 20   # mm
outer_height = 40  # mm
wall_thickness = 2 # mm

# Calculate inner box dimensions
inner_length = outer_length - 2 * wall_thickness
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - wall_thickness  # Open at the top

# Create outer and inner boxes
outer_box = trimesh.primitives.Box(extents=[outer_length, outer_width, outer_height])
inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])

# Position inner box centered within outer box
inner_box.apply_translation([0, 0, wall_thickness/2])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure mesh is watertight and valid for 3D printing
hollow_box = hollow_box.process(validate=True)

# Export as STL
hollow_box.export('output.stl')