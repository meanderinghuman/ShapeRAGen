import trimesh
import numpy as np

# Parameters with explicit units (mm)
outer_radius = 15.0
inner_radius = 14.0
height = 40.0
segments = 64  # For smoother circles

# Create cylinders with explicit segment count
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

# Center both cylinders at origin
outer_cylinder.apply_translation([0, 0, -height/2])
inner_cylinder.apply_translation([0, 0, -height/2])

# Verify wall thickness meets minimum requirements (typically >0.8mm for FDM)
wall_thickness = outer_radius - inner_radius
if wall_thickness < 0.8:
    raise ValueError(f"Wall thickness {wall_thickness}mm is below minimum recommended for FDM printing")

# Perform boolean difference with error handling
try:
    hollow_cylinder = outer_cylinder.difference(inner_cylinder)
except:
    raise RuntimeError("Boolean operation failed - check mesh validity")

# Validate and repair mesh
hollow_cylinder.process(validate=True)
if not hollow_cylinder.is_watertight:
    hollow_cylinder.fill_holes()
    hollow_cylinder.process(validate=True)

# Final validation
assert hollow_cylinder.is_watertight, "Mesh is not watertight"
assert hollow_cylinder.volume > 0, "Mesh has zero volume"

# Export as STL
hollow_cylinder.export('output.stl')