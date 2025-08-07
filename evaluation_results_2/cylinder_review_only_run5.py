import trimesh
import numpy as np

# Parameters with explicit values for better control
outer_radius = 15.0
inner_radius = 14.0
height = 40.0
segments = 64  # Higher count for smoother circles
min_wall_thickness = 1.0  # Minimum recommended for FDM printing

# Verify wall thickness meets minimum requirements
assert (outer_radius - inner_radius) >= min_wall_thickness, "Wall thickness below minimum recommended"

# Create cylinders with explicit segments
outer_cylinder = trimesh.creation.cylinder(
    radius=outer_radius,
    height=height,
    sections=segments
)

inner_cylinder = trimesh.creation.cylinder(
    radius=inner_radius,
    height=height * 1.01,  # Slightly taller for clean boolean
    sections=segments
)

# Perform boolean difference with validation
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Verify boolean operation succeeded
if not hollow_cylinder.is_volume:
    raise ValueError("Boolean operation failed to create a valid volume")

# Ensure mesh is printable
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Additional validation
if not hollow_cylinder.is_watertight:
    raise ValueError("Resulting mesh is not watertight")

if hollow_cylinder.volume <= 0:
    raise ValueError("Resulting mesh has no volume")

# Export with explicit file type
hollow_cylinder.export('output.stl', file_type='stl')