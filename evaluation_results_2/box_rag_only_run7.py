import trimesh
import numpy as np
from stl import mesh

# Create outer box dimensions
outer_length = 30  # x dimension
outer_width = 20   # y dimension
outer_height = 40  # z dimension
wall_thickness = 1.2  # recommended minimum for FDM printing

# Create inner box dimensions (hollow space)
inner_length = outer_length - (2 * wall_thickness)
inner_width = outer_width - (2 * wall_thickness)
inner_height = outer_height - wall_thickness  # leave bottom solid

# Create outer box mesh
outer_box = trimesh.primitives.Box(extents=[outer_length, outer_width, outer_height])

# Create inner box mesh (offset by wall thickness)
inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])
inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight and valid for 3D printing
hollow_box.process(validate=True)

# Export as STL file
hollow_box.export('output.stl')