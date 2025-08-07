import trimesh
import numpy as np
from stl import mesh

# Define outer dimensions
outer_length = 30
outer_width = 20
outer_height = 40

# Define wall thickness (2mm is good for FDM printing)
wall_thickness = 2
min_wall_thickness = 0.4  # Typical nozzle diameter

# Validate wall thickness
if wall_thickness < min_wall_thickness:
    raise ValueError(f"Wall thickness must be at least {min_wall_thickness}mm for FDM printing")

# Create outer box
outer_box = trimesh.primitives.Box(extents=[outer_length, outer_width, outer_height])

# Create inner box dimensions
inner_length = outer_length - 2 * wall_thickness
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - wall_thickness

# Create inner box (positioned slightly above the bottom)
inner_box = trimesh.primitives.Box(extents=[inner_length, inner_width, inner_height])
inner_box.apply_translation([0, 0, wall_thickness])

# Subtract inner box from outer box to create hollow box
hollow_box = outer_box.difference(inner_box)

# Ensure mesh is watertight and manifold
hollow_box = hollow_box.process(validate=True)

# Add optional support structure
support_height = 5
support_thickness = 2
if outer_height > 50:  # Add supports if tall object
    support = trimesh.primitives.Box(extents=[support_thickness, outer_width, support_height])
    support.apply_translation([(outer_length/2 + support_thickness/2), 0, 0])
    hollow_box = hollow_box.union(support)

# Verify mesh before export
if not hollow_box.is_watertight:
    hollow_box.fill_holes()
    hollow_box = hollow_box.process(validate=True)

# Export as STL
hollow_box.export('output.stl')