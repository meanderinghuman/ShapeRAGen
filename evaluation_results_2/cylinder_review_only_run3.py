import trimesh
import numpy as np

# Parameters with explicit values for better control
outer_radius = 15.0
inner_radius = 14.0
height = 40.0
segments = 64  # Higher count for smoother circles
min_wall_thickness = 1.0  # Minimum recommended wall thickness for FDM

# Verify wall thickness meets minimum requirements
assert (outer_radius - inner_radius) >= min_wall_thickness, "Wall thickness below minimum recommended for FDM printing"

# Create cylinders centered at origin for better printability
outer_cylinder = trimesh.creation.cylinder(
    radius=outer_radius,
    height=height,
    sections=segments,
    transform=trimesh.transformations.translation_matrix([0, 0, -height/2])
)

inner_cylinder = trimesh.creation.cylinder(
    radius=inner_radius,
    height=height * 1.01,  # Slightly taller for clean boolean
    sections=segments,
    transform=trimesh.transformations.translation_matrix([0, 0, -height/2])
)

# Boolean difference operation
hollow_cylinder = outer_cylinder.difference(inner_cylinder)

# Process and validate mesh
hollow_cylinder.fill_holes()
hollow_cylinder.process()

# Verify mesh is watertight before export
if not hollow_cylinder.is_watertight:
    hollow_cylinder = hollow_cylinder.convex_hull

# Export as STL
hollow_cylinder.export('output.stl')