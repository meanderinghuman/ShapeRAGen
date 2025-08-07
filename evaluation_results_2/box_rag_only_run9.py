import trimesh
import numpy as np
from stl import mesh

# Create outer box dimensions
outer_dimensions = [20, 30, 40]
wall_thickness = 2.0  # 2mm wall thickness for FDM printing

# Calculate inner box dimensions
inner_dimensions = [d - 2 * wall_thickness for d in outer_dimensions]

# Create outer and inner boxes
outer_box = trimesh.primitives.Box(extents=outer_dimensions)
inner_box = trimesh.primitives.Box(extents=inner_dimensions)

# Position the inner box centered within the outer box
inner_box.apply_translation([wall_thickness, wall_thickness, wall_thickness])

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.difference(inner_box)

# Ensure the mesh is watertight (important for 3D printing)
hollow_box.fill_holes()
hollow_box.fix_normals()

# Export as STL file
hollow_box.export('output.stl')